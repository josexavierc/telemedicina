import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

type Spec = { id:number; name:string; description:string }

export default function Specialties(){
  const [items, setItems] = useState<Spec[]>([])
  const [q, setQ] = useState('')

  useEffect(()=>{ api<Spec[]>(`/specialties/?q=${encodeURIComponent(q)}`).then(setItems) },[q])

  return (
    <div className="p-6 max-w-3xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Especialidades</h1>
      <input className="border p-2 rounded w-full" placeholder="Buscar..." value={q} onChange={e=>setQ(e.target.value)} />
      <ul className="divide-y border rounded">
        {items.map(s => (
          <li key={s.id} className="p-3">
            <div className="font-medium">{s.name}</div>
            <div className="text-sm text-gray-600">{s.description}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
