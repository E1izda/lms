import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api/api'

export default function CourseDetail() {
  const { id } = useParams()
  const [course, setCourse] = useState(null)

  useEffect(() => {
    api.get(`/api/v1/courses/${id}/`)
      .then(res => setCourse(res))
      .catch(err => console.error(err))
  }, [id])

  if (!course) return <div>Loading...</div>

  return (
    <div>
      <h1>{course.title}</h1>
      <p>{course.description}</p>
      <p>Price: {course.price}</p>
    </div>
  )
}
