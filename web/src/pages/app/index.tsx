import { ChevronUp } from "lucide-react"
import { Drop } from "../../components/Drop"
import "./style.scss"

export function App() {
  function handleScroll(elementId: string) {
    const element = document.getElementById(elementId)

    if (element) element.scrollIntoView({ behavior: "smooth" })
  }

  return (
    <main className="page">
      <header>
        <button>Equipe</button>
      </header>
      <section id="home">
        <div>
          <div>
            <h1>
              <span>Reconhecimento</span> Facial
            </h1>
            <p>
              IA para reconhecimento de rostos usando <span>Octave</span> e{" "}
              <span>OpenCV</span>
            </p>
          </div>
          <button onClick={() => handleScroll("recognition")}>Testar</button>
        </div>
        <img src="/head.svg" width={500} alt="" />
      </section>

      <section id="recognition">
        <Drop />

        <button className="back" onClick={() => handleScroll("home")}>
          <ChevronUp />
        </button>
      </section>
    </main>
  )
}
