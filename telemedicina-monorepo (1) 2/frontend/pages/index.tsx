import { useState, useEffect } from 'react'
import { login } from '@/lib/api'
import { useRouter } from 'next/router'

export default function Home() {
  const [email, setEmail] = useState('admin@demo.local')
  const [password, setPassword] = useState('Admin123!')
  const [error, setError] = useState<string | null>(null)
  const r = useRouter()

  async function onLogin(e:any){
    e.preventDefault()
    setError(null)
    try {
      const tok = await login(email, password)
      localStorage.setItem('token', tok.access_token)
      r.push('/dashboard')
    } catch (e:any) {
      setError(e.message || 'Error')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={onLogin} className="bg-white p-8 rounded-xl shadow w-[380px] space-y-4">
        <h1 className="text-2xl font-bold text-center">Telemed — Ingresar</h1>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <input className="border w-full p-2 rounded" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="border w-full p-2 rounded" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="w-full py-2 rounded bg-black text-white">Entrar</button>
        <p className="text-xs text-gray-500">Demo: admin@demo.local / Admin123!</p>
      </form>
    </div>
  )
}
