export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"

export async function api<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const token = (typeof window !== 'undefined') ? localStorage.getItem('token') : null;
  const headers: Record<string,string> = { 'Content-Type': 'application/json', ...(opts.headers as any) }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function login(username: string, password: string) {
  const body = new URLSearchParams({ username, password })
  const res = await fetch(`${API_BASE}/auth/token`, { method: 'POST', body })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}
