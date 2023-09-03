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

import { ImageType } from "@app/recognize/page"
import { CAMERA_FLAG, PHOTO_NAME, VIDEO_CONSTRAINTS } from "@constants/camera"
import { Preview } from "./Preview"

import Webcam from "react-webcam"

interface DropProps {
  image: ImageType
  setImage: Dispatch<SetStateAction<ImageType>>
}

export function Drop({ image, setImage }: DropProps) {
  const [cameraOpen, setCameraOpen] = useState(false)

  const dropHandler = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length) {
        const [file] = acceptedFiles
        setImage(Object.assign(file, { preview: URL.createObjectURL(file) }))
      }
    },
    [setImage]
  )

  const { getRootProps, getInputProps, open } = useDropzone({
    noClick: true,
    noKeyboard: true,
    multiple: false,
    accept: { ["image/*"]: [] },
    onDrop: dropHandler,
  })

  const webcamRef = useRef<Webcam>(null)

  const takePhoto = () => (!cameraOpen ? setCameraOpen(true) : capture())

  const capture = useCallback(() => {
    const src = webcamRef.current?.getScreenshot()
    const photoName = PHOTO_NAME

    if (src) setImage(Object.assign(new File([], photoName), { preview: src }))

    setCameraOpen(false)
  }, [webcamRef, setImage])

  useEffect(() => () => URL.revokeObjectURL(image?.preview ?? ""), [image])

  const isCameraImage = image?.preview.includes(CAMERA_FLAG)

  return (
    <div
      className={`flex flex-col items-center gap-4 ${
        image ? "pb-4 px-2 pt-2" : "p-4"
      } bg-slate-200 max-w-[50%] ${
        !isCameraImage && "w-[35%]"
      } text-rose-950 rounded-xl`}
    >
      <div
        {...getRootProps({ className: "dropzone" })}
        className={`flex flex-col justify-center items-center rounded-lg  ${
          image ? "w-fit" : "p-5 w-full"
        } bg-rose-600/20 border-rose-600 border-dashed border-2 text-rose-900`}
      >
        {!image ? (
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
                videoConstraints={VIDEO_CONSTRAINTS}
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
          <Preview image={image} setImage={setImage} />
        )}
      </div>
      {image && <h4 className="text-rose-500 font-medium">{image?.name}</h4>}
    </div>
  )
}
