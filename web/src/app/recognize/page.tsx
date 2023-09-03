"use client"

import "react-toastify/dist/ReactToastify.css"

import { useState } from "react"
import { ToastContainer, toast } from "react-toastify"

import { Drop } from "@components/Drop"
import { TOAST_OPTIONS } from "@constants/toast"

export type ImageType = (File & { preview: string }) | null
export type FileUploadResponse = { success: boolean; path: string }

export default function RecognizePage() {
  const [image, setImage] = useState<ImageType>(null)

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

      <ToastContainer />
    </main>
  )
}
