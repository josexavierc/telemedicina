import type { AppProps } from 'next/app'
import '@/styles/globals.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const qc = new QueryClient()

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={qc}>
      <Component {...pageProps} />
    </QueryClientProvider>
  )
}
