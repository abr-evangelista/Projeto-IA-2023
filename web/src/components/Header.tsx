import Link from "next/link"

export function Header() {
  return (
    <header className="h-24 w-full flex justify-end items-center px-8 absolute z-10">
      <Link
        href="/"
        className="text-xl font-bold px-8 py-2 bg-transparent hover:text-rose-600 transition-all"
      >
        Home
      </Link>
      <Link
        href="recognize"
        className="text-xl font-bold px-8 py-2 bg-transparent hover:text-rose-600 transition-all cursor-pointer"
      >
        Testar
      </Link>
      <Link
        href="/"
        className="text-xl font-bold px-8 py-2 bg-transparent hover:text-rose-600 transition-all"
      >
        Equipe
      </Link>
    </header>
  )
}
