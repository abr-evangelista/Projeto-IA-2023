import { FileType } from "@/app/recognize/page"
import { X } from "lucide-react"
import Image from "next/image"

interface PreviewProps {
  file: FileType
  setFiles: React.Dispatch<React.SetStateAction<FileType[]>>
}

export function Preview({ file, setFiles }: PreviewProps) {
  return (
    <div className="relative flex flex-col justify-center items-center h-full">
      <button
        className="p-2 bg-rose-500 rounded-full absolute -top-4 -right-4 hover:bg-rose-500/80 transition-all duration-500"
        onClick={() => setFiles([])}
      >
        <X className="text-white w-6 h-6" />
      </button>
      <Image
        src={file.preview}
        alt="Preview da imagem"
        className="w-full h-full rounded-lg"
        width={0}
        height={0}
        sizes="100vw"
        onLoad={() => URL.revokeObjectURL(file.preview)}
      />
    </div>
  )
}
