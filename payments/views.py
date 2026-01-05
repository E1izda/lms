from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import stripe
from .models import Payment
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request, course_id):
    from courses.models import Course
    try:
        course = Course.objects.get(id=course_id)
        if course.price == 0:
            return Response({'error': 'Course is free'}, status=status.HTTP_400_BAD_REQUEST)

        intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),  # Amount in cents
            currency='usd',
            metadata={'course_id': course_id, 'user_id': request.user.id}
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            stripe_payment_intent_id=intent.id
        )

        return Response({
            'client_secret': intent.client_secret,
            'payment_id': payment.id
        })
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
        intent = stripe.PaymentIntent.retrieve(payment.stripe_payment_intent_id)

        if intent.status == 'succeeded':
            payment.status = 'completed'
            payment.save()
            return Response(PaymentSerializer(payment).data)
        else:
            return Response({'error': 'Payment not completed'}, status=status.HTTP_400_BAD_REQUEST)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
