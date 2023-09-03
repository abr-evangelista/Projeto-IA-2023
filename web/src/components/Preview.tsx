import Image from "next/image"
import { Dispatch, SetStateAction } from "react"

import { ImageType } from "@app/recognize/page"
import { X } from "lucide-react"

interface PreviewProps {
  image: ImageType
  setImage: Dispatch<SetStateAction<ImageType>>
}

export function Preview({ image, setImage }: PreviewProps) {
  return (
    <div className="relative flex flex-col justify-center items-center h-full">
      <button
        className="p-2 bg-rose-500 rounded-full absolute -top-4 -right-4 hover:bg-rose-500/80 transition-all duration-500"
        onClick={() => setImage(null)}
      >
        <X className="text-white w-6 h-6" />
      </button>
      <Image
        src={image?.preview ?? ""}
        alt="Preview da imagem"
        className="w-full h-full rounded-lg"
        width={0}
        height={0}
        sizes="100vw"
        onLoad={() => URL.revokeObjectURL(image?.preview ?? "")}
      />
    </div>
  )
}
