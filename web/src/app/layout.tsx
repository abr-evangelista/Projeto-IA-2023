import "../styles/globals.css"

import { Header } from "@components/Header"

import type { Metadata } from "next"
import { Inter } from "next/font/google"

const inter = Inter({ subsets: ["latin"], fallback: ["latin"] })

export const metadata: Metadata = {
  title: "IA - Reconhecimento Facial",
  description: "Modelo de reconhecimento facial para IA",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-br">
      <body className={inter.className}>
        <Header />
        {children}
      </body>
    </html>
  )
}
