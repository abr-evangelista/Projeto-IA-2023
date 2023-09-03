import { useDropzone } from "react-dropzone"

import { ImageIcon } from "lucide-react"
import {
  Dispatch,
  SetStateAction,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react"

import { FileType } from "@/app/recognize/page"
import Webcam from "react-webcam"
import { Preview } from "./Preview"

interface DropProps {
  files: FileType[]
  setFiles: Dispatch<SetStateAction<FileType[]>>
}

export function Drop({ files, setFiles }: DropProps) {
  const [cameraOpen, setCameraOpen] = useState(false)
  const [photoSrc, setPhotoSrc] = useState<string | null>(null)

  const webcamRef = useRef<Webcam>(null)

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user",
  }

  const dropHandler = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length) {
        setFiles((previousFiles) => [
          ...previousFiles,
          ...acceptedFiles.map((file) =>
            Object.assign(file, {
              preview: URL.createObjectURL(file),
              photoSrc: "",
            })
          ),
        ])
      }
    },
    [setFiles]
  )

  const { getRootProps, getInputProps, open } = useDropzone({
    noClick: true,
    noKeyboard: true,
    multiple: false,
    accept: { ["image/*"]: [] },
    onDrop: dropHandler,
  })

  const takePhoto = () => {
    if (cameraOpen) {
      capture()
      setCameraOpen(false)
    } else {
      setCameraOpen(true)
    }
  }

  const capture = useCallback(() => {
    const src = webcamRef.current?.getScreenshot()
    if (src) {
      setPhotoSrc(src)
      setFiles((previousFiles) => [
        ...previousFiles,
        Object.assign(new File([], "photo.jpg"), {
          preview: src,
          photoSrc: src,
        }),
      ])
    }
  }, [webcamRef, setFiles])

  useEffect(() => {
    return () => files.forEach((file) => URL.revokeObjectURL(file.preview))
  }, [files])

  const hasFile = files.length > 0

  return (
    <div
      className={`flex flex-col items-center gap-4 ${
        hasFile ? "pb-4 px-2 pt-2" : "p-4"
      } bg-slate-200 max-w-[50%] ${
        !!!files[0]?.photoSrc && "w-[35%]"
      } text-rose-950 rounded-xl`}
    >
      <div
        {...getRootProps({ className: "dropzone" })}
        className={`flex flex-col justify-center items-center rounded-lg  ${
          hasFile ? "w-fit" : "p-5 w-full"
        } bg-rose-600/20 border-rose-600 border-dashed border-2 text-rose-900`}
      >
        {files.length === 0 ? (
          <div className="flex flex-col items-center gap-3">
            <ImageIcon className="text-rose-500 w-12 h-12" />
            <input {...getInputProps()} dir="" />
            <p className="text-lg font-semibold">
              Arraste e solte a imagem aqui
            </p>
            <span className="font-normal flex items-center uppercase before:content-[' '] before:bg-[#8d1a3b] before:text-[#8d1a3b80] before:m-2 before:p-[0.5px] before:w-20 after:content-[' '] after:bg-[#8d1a3b] after:text-[#8d1a3b80] after:m-2 after:p-[0.5px] after:w-20">
              ou
            </span>
            <button
              className="p-4 min-w-[170px] rounded-lg bg-rose-500 text-white text-base font-medium hover:brightness-90 transition-all duration-500"
              onClick={open}
            >
              Procurar imagem...
            </button>
            <span className="font-normal flex items-center uppercase before:content-[' '] before:bg-[#8d1a3b] before:text-[#8d1a3b80] before:m-2 before:p-[0.5px] before:w-20 after:content-[' '] after:bg-[#8d1a3b] after:text-[#8d1a3b80] after:m-2 after:p-[0.5px] after:w-20">
              ou
            </span>
            {cameraOpen && (
              <Webcam
                ref={webcamRef}
                videoConstraints={videoConstraints}
                screenshotFormat="image/jpeg"
                audio={false}
                className="rounded-lg"
              />
            )}
            <button
              className="p-4 min-w-[170px] rounded-lg bg-rose-500 text-white text-base font-medium hover:brightness-90 transition-all duration-500"
              onClick={takePhoto}
            >
              Tirar foto...
            </button>
          </div>
        ) : (
          <Preview file={files[0]} setFiles={setFiles} />
        )}
      </div>
      {files.length > 0 && (
        <h4 className="text-rose-500 font-medium">{files[0].name}</h4>
      )}
    </div>
  )
}
