"use client"

import { Drop } from "@/components/Drop"
import { useState } from "react"
import { ToastContainer, ToastOptions, toast } from "react-toastify"

import "react-toastify/dist/ReactToastify.css"

export type FileType = { preview: string; photoSrc: string } & File

export type FileUploadResponse = { success: boolean; path: string }

export default function RecognizePage() {
  const [files, setFiles] = useState<FileType[]>([])

  const toastOptions: ToastOptions = {
    position: "bottom-right",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
    theme: "colored",
  }

  const submitHandler = async () => {
    const formData = new FormData()

    files.forEach((file) => {
      formData.append("file", file)
      formData.append("photoSrc", file.photoSrc)
    })

    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    })

    const { success }: FileUploadResponse = await response.json()

    if (success) {
      toast.success(
        `Upload da imagem ${files[0].name} realizada com sucesso!`,
        toastOptions
      )
    } else {
      toast.error(
        `Erro ao realizar upload da imagem ${files[0].name}!`,
        toastOptions
      )
    }
  }

  return (
    <main className="pt-24 relative flex flex-col items-center gap-10">
      <Drop files={files} setFiles={setFiles} />

      {files.length > 0 && (
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
