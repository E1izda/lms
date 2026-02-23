import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/api'

export default function Courses() {
  const [courses, setCourses] = useState([])

  useEffect(() => {
    api.get('/api/v1/courses/')
      .then(res => setCourses(res))
      .catch(err => console.error(err))
  }, [])

  return (
    <div>
      <h1>Courses</h1>
      <ul>
        {courses.map(c => (
          <li key={c.id}>
            <Link to={`/courses/${c.id}`}>{c.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
