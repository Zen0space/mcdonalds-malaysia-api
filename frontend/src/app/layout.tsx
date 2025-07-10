import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: "McDonald's Malaysia Map",
  description: 'Simple map showing McDonald\'s outlets in Malaysia',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  )
} 