import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/api'

export default function Login(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    try{
      const data = await api.post('/api/v1/auth/login/', { username, password })
      // expect { access: 'token' } or similar
      const token = data.access || data.token || data.key
      if(token){
        localStorage.setItem('access_token', token)
        navigate('/')
      } else {
        alert('Login failed')
      }
    }catch(err){
      console.error(err)
      alert('Login error')
    }
  }

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={submit}>
        <div>
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  )
}
