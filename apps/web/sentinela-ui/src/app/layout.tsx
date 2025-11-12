import './globals.css'
import Providers from '@/components/Providers'

export const metadata = {
  title: 'Sentinela IAM',
  description: 'Identity and Access Management System',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
