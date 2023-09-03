import Image from "next/image"
import Link from "next/link"

export default function HomePage() {
  return (
    <main className="flex justify-around items-center h-screen">
      <div className="flex flex-col items-start gap-8">
        <div className="flex flex-col gap-2">
          <h1 className="text-6xl font-bold mb-4">
            <span className="text-rose-600">Reconhecimento</span> Facial
          </h1>
          <p className="text-2xl font-normal mb-4">
            IA para reconhecimento de rostos usando{" "}
            <span className="text-rose-600">Octave</span> e{" "}
            <span className="text-rose-600">OpenCV</span>
          </p>
        </div>
        <Link
          href="/recognize"
          className="bg-rose-600 px-8 rounded-xl py-4 text-2xl hover:brightness-90 transition-all duration-500"
          passHref
        >
          Testar
        </Link>
      </div>
      <Image src="/head.svg" width={500} height={500} alt="head" priority />
    </main>
  )
}
