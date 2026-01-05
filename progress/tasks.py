from celery import shared_task
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from django.core.files.base import ContentFile
from .models import CourseProgress
import io

@shared_task
def generate_certificate(progress_id):
    try:
        progress = CourseProgress.objects.get(id=progress_id)
        if not progress.is_completed:
            return None

        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center
        )

        content_style = ParagraphStyle(
            'Content',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=20,
            alignment=1
        )

        story = []

        # Title
        story.append(Paragraph("Certificate of Completion", title_style))
        story.append(Spacer(1, 0.5*inch))

        # Content
        story.append(Paragraph(f"This certifies that", content_style))
        story.append(Paragraph(f"<b>{progress.user.get_full_name()}</b>", content_style))
        story.append(Paragraph("has successfully completed the course", content_style))
        story.append(Paragraph(f"<b>{progress.course.title}</b>", content_style))
        story.append(Paragraph(f"on {progress.completed_at.strftime('%B %d, %Y')}", content_style))

        doc.build(story)

        # Save PDF to model
        buffer.seek(0)
        progress.certificate_file.save(
            f'certificate_{progress.user.username}_{progress.course.id}.pdf',
            ContentFile(buffer.getvalue())
        )
        progress.certificate_issued = True
        progress.save()

        return progress.certificate_file.url

    except CourseProgress.DoesNotExist:
        return None