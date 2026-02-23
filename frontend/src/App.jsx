import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Courses from './pages/Courses'
import CourseDetail from './pages/CourseDetail'
import Login from './pages/Login'

export default function App() {
  return (
    <div className="app">
      <nav>
        <Link to="/">Courses</Link>
        <Link to="/login">Login</Link>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Courses />} />
          <Route path="/courses/:id" element={<CourseDetail />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </main>
    </div>
  )
}
