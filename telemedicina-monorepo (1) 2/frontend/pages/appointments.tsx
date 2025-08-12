import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

type AppointmentOut = { id:number; scheduled_at:string; duration_minutes:number; status:string; room_id?:string }

export default function Appointments(){
  const [items, setItems] = useState<AppointmentOut[]>([])
  useEffect(()=>{ api<AppointmentOut[]>('/appointments/').then(setItems) },[])
  return (
    <div className="p-6 max-w-3xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Citas</h1>
      <div className="space-y-2">
        {items.map(a => (
          <div key={a.id} className="border rounded p-3">
            <div className="font-medium">{new Date(a.scheduled_at).toLocaleString()}</div>
            <div className="text-sm text-gray-600">{a.duration_minutes} min — {a.status}</div>
            {a.room_id && <a className="underline" href={`/video/${a.room_id}`}>Entrar a sala</a>}
          </div>
        ))}
      </div>
    </div>
  )
}
