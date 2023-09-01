import { useDropzone } from "react-dropzone"

import { Image } from "lucide-react"
import "./style.scss"

export function Drop() {
  const { getRootProps, getInputProps, open, acceptedFiles } = useDropzone({
    noClick: true,
    noKeyboard: true,
  })

  const files = acceptedFiles.map((file) => (
    <li key={file.name}>
      {file.name} - {file.size} bytes
    </li>
  ))

  return (
    <div className="container">
      <div {...getRootProps({ className: "dropzone" })}>
        <Image />
        <input {...getInputProps()} />
        <p>Arraste e solte a imagem aqui</p>
        <div>ou</div>
        <button onClick={open}>Procurar imagem...</button>
        <div>ou</div>
        <button>Tirar foto...</button>
      </div>
      {files.length > 0 && (
        <aside>
          <h4>Files</h4>
          <p>{files}</p>
        </aside>
      )}
    </div>
  )
}
