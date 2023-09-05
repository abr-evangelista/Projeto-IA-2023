"use client"

import "react-toastify/dist/ReactToastify.css"

import { useEffect, useState } from "react"
import { ToastContainer, toast } from "react-toastify"

import { Drop } from "@components/Drop"
import { TOAST_OPTIONS } from "@constants/toast"
import Image from "next/image"

export type ImageType = (File & { preview: string }) | null
export type FileUploadResponse = { success: boolean; path: string }

export default function RecognizePage() {
  const [image, setImage] = useState<ImageType>(null)
  const [imageProcessed, setImageProcessed] = useState<boolean>(false)
  const [src, setSrc] = useState("/outs/result.png")
  const [updateCount, setUpdateCount] = useState(0)

  useEffect(() => {
    if (imageProcessed && updateCount < 100) {
      fetch("/outs/result.png")
        .then((response) => response.blob())
        .then((blob) => {
          setSrc(URL.createObjectURL(blob))
          setUpdateCount((count) => count + 1)
        })
    }
  }, [src, updateCount, imageProcessed])

  const submitHandler = async () => {
    if (!image) return

    const formData = new FormData()

    formData.append("image", image)
    formData.append("preview", image.preview)

    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    })

    const { success }: FileUploadResponse = await response.json()

    if (success) {
      toast.success(
        `Upload da imagem ${image.name} realizada com sucesso!`,
        TOAST_OPTIONS
      )
    } else {
      toast.error(
        `Erro ao realizar upload da imagem ${image.name}!`,
        TOAST_OPTIONS
      )
    }

    setImageProcessed(success)
  }

  return (
    <main className="pt-24 relative flex flex-col items-center gap-10">
      <Drop image={image} setImage={setImage} />

      {image && (
        <button
          className="px-4 py-3 min-w-[170px] rounded-lg bg-rose-500 text-white text-base font-medium hover:brightness-90 transition-all duration-500"
          onClick={submitHandler}
        >
          Reconhecer
        </button>
      )}

      {imageProcessed && image && (
        <div className="flex flex-col gap-5">
          <h2 className="text-2xl font-bold text-center">Imagem processada</h2>
          <Image
            src={src}
            className="w-full h-full rounded-lg border-rose-600 border-4 shadow-xl"
            width={0}
            height={0}
            sizes="100vw"
            alt="Imagem processada"
          />
        </div>
      )}
      <ToastContainer />
    </main>
  )
}
