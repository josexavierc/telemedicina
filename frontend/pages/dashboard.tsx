import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import Link from 'next/link'

type Appointment = {
  id: number;
  scheduled_at: string;
  duration_minutes: number;
  status: string;
  room_id?: string;
}

export default function Dashboard() {
  const [appts, setAppts] = useState<Appointment[]>([])
  const [error, setError] = useState<string|null>(null)

  useEffect(() => {
    api<Appointment[]>('/appointments/').then(setAppts).catch(e=>setError(String(e)))
  }, [])

  return (
    <div className="p-6 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Panel</h1>
        <nav className="space-x-4">
          <Link className="underline" href="/specialties">Especialidades</Link>
          <Link className="underline" href="/appointments">Citas</Link>
          <Link className="underline" href="/video/new">Teleconsulta</Link>
        </nav>
      </header>

      <section>
        <h2 className="text-xl font-semibold mb-2">Mis citas</h2>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="grid md:grid-cols-2 gap-4">
          {appts.map(a => (
            <div key={a.id} className="rounded-xl border p-4">
              <div className="font-medium">{new Date(a.scheduled_at).toLocaleString()}</div>
              <div className="text-sm text-gray-600">{a.duration_minutes} min — {a.status}</div>
              {a.room_id && <Link className="text-sm underline" href={`/video/${a.room_id}`}>Entrar a sala</Link>}
            </div>
          ))}
          {appts.length===0 && <p className="text-sm text-gray-500">Sin citas aún.</p>}
        </div>
      </section>
    </div>
  )
}
