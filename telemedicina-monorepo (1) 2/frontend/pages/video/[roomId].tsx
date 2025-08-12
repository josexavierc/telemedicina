
import { useEffect, useRef, useState } from 'react'
import { API_BASE } from '@/lib/api'
import { useRouter } from 'next/router'

type Signal = any

export default function Room(){
  const { query } = useRouter()
  const roomId = (query.roomId as string) || ''
  const localVideo = useRef<HTMLVideoElement>(null)
  const remoteVideo = useRef<HTMLVideoElement>(null)
  const pc = useRef<RTCPeerConnection | null>(null)
  const ws = useRef<WebSocket | null>(null)
  const [ready, setReady] = useState(false)
  const [chat, setChat] = useState<string[]>([])
  const [msg, setMsg] = useState('')
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const drawing = useRef(false)
  const [screenOn, setScreenOn] = useState(false)

  useEffect(() => {
    if (!roomId) return
    const wsUrl = API_BASE.replace(/^http/, 'ws') + `/teleconsult/ws/${roomId}`
    ws.current = new WebSocket(wsUrl)
    ws.current.onmessage = async (event) => {
      const msg: Signal = JSON.parse(event.data)
      if (msg.type === 'offer' || msg.type === 'answer') {
        if (!pc.current) return
        await pc.current.setRemoteDescription(msg)
        if (msg.type === 'offer') {
          const ans = await pc.current.createAnswer()
          await pc.current.setLocalDescription(ans)
          ws.current?.send(JSON.stringify(ans))
        }
      } else if ((msg as any).candidate) {
        try { await pc.current?.addIceCandidate(msg) } catch {}
      } else if (msg.chat) {
        setChat(c => [...c, msg.chat])
      } else if (msg.wb) {
        const ctx = canvasRef.current?.getContext('2d')
        if (!ctx) return
        const {x0,y0,x1,y1} = msg.wb
        ctx.beginPath()
        ctx.moveTo(x0, y0)
        ctx.lineTo(x1, y1)
        ctx.stroke()
        ctx.closePath()
      }
    }
    ws.current.onopen = () => setReady(true)
    return () => ws.current?.close()
  }, [roomId])

  useEffect(() => {
    async function run(){
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      if (localVideo.current) localVideo.current.srcObject = stream

      pc.current = new RTCPeerConnection()
      stream.getTracks().forEach(t => pc.current!.addTrack(t, stream))
      pc.current.ontrack = (e) => {
        if (remoteVideo.current) remoteVideo.current.srcObject = e.streams[0]
      }
      pc.current.onicecandidate = (e) => {
        if (e.candidate) ws.current?.send(JSON.stringify({ candidate: e.candidate }))
      }
      if (ready) {
        const offer = await pc.current.createOffer()
        await pc.current.setLocalDescription(offer)
        ws.current?.send(JSON.stringify(offer))
      }
    }
    run()
  }, [ready])

  function sendChat(){
    if (!msg.trim()) return
    ws.current?.send(JSON.stringify({ chat: msg }))
    setChat(c => [...c, `Yo: ${msg}`])
    setMsg('')
  }

  function onCanvasMouseDown(e: React.MouseEvent<HTMLCanvasElement>){
    drawing.current = true
  }
  function onCanvasMouseUp(){
    drawing.current = false
  }
  function onCanvasMouseMove(e: React.MouseEvent<HTMLCanvasElement>){
    if (!drawing.current) return
    const rect = (e.target as HTMLCanvasElement).getBoundingClientRect()
    const x1 = e.clientX - rect.left; const y1 = e.clientY - rect.top
    const ctx = canvasRef.current?.getContext('2d')
    if (!ctx) return
    const x0 = (canvasRef.current as any)._lx || x1
    const y0 = (canvasRef.current as any)._ly || y1
    ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.stroke(); ctx.closePath()
    ;(canvasRef.current as any)._lx = x1; (canvasRef.current as any)._ly = y1
    ws.current?.send(JSON.stringify({ wb: { x0,y0,x1,y1 } }))
  }

  async function shareScreen(){
    if (screenOn) return
    const stream = await (navigator.mediaDevices as any).getDisplayMedia({ video: true, audio: false })
    const track = stream.getVideoTracks()[0]
    const sender = pc.current?.getSenders().find(s => s.track?.kind === 'video')
    await sender?.replaceTrack(track)
    setScreenOn(true)
    track.onended = async () => {
      const cam = (localVideo.current?.srcObject as MediaStream).getVideoTracks()[0]
      await sender?.replaceTrack(cam)
      setScreenOn(false)
    }
  }

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Sala: {roomId}</h1>
      <div className="grid md:grid-cols-2 gap-4">
        <video ref={localVideo} autoPlay muted className="w-full bg-black rounded" />
        <video ref={remoteVideo} autoPlay className="w-full bg-black rounded" />
      </div>

      <div className="flex gap-2">
        <button onClick={shareScreen} className="px-3 py-2 rounded bg-black text-white">{screenOn ? 'Compartiendo pantalla' : 'Compartir pantalla'}</button>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="border rounded p-3">
          <h2 className="font-semibold mb-2">Chat</h2>
          <div className="h-40 overflow-auto border rounded p-2 mb-2 bg-gray-50">
            {chat.map((c,i)=>(<div key={i} className="text-sm">{c}</div>))}
          </div>
          <div className="flex gap-2">
            <input className="border p-2 rounded flex-1" value={msg} onChange={e=>setMsg(e.target.value)} placeholder="Escribe un mensaje..." />
            <button onClick={sendChat} className="px-3 py-2 rounded bg-black text-white">Enviar</button>
          </div>
        </div>
        <div className="border rounded p-3">
          <h2 className="font-semibold mb-2">Pizarra</h2>
          <canvas ref={canvasRef} width={600} height={300}
            className="border rounded w-full"
            onMouseDown={onCanvasMouseDown}
            onMouseUp={onCanvasMouseUp}
            onMouseMove={onCanvasMouseMove}
          />
        </div>
      </div>
    </div>
  )
}
