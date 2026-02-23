const API_BASE = import.meta.env.VITE_API_BASE || ''

async function request(path, options = {}){
  const headers = options.headers || {}
  const token = localStorage.getItem('access_token')
  if(token) headers['Authorization'] = `Bearer ${token}`
  headers['Content-Type'] = headers['Content-Type'] || 'application/json'

  const res = await fetch(API_BASE + path, { ...options, headers })
  if(res.status === 204) return null
  const data = await res.json()
  if(!res.ok) throw data
  return data
}

export default {
  get: (path) => request(path, { method: 'GET' }),
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
}
