import { promises as fsPromises } from "fs"
import { NextResponse } from "next/server"
import { join } from "path"

import { ImageType } from "@app/recognize/page"
import { CAMERA_FLAG } from "@constants/camera"

export async function POST(request: Request) {
  try {
    const formData = await request.formData()

    const image: ImageType = formData.get("image") as unknown as ImageType
    const preview: string = formData.get("preview") as unknown as string

    if (!image) {
      return NextResponse.json({
        success: false,
        error: "Nenhum arquivo foi enviado.",
      })
    }

    let buffer: Buffer

    const isCameraImage = preview.includes(CAMERA_FLAG)

    if (isCameraImage) {
      const base64Data = preview.replace(/^data:image\/\w+;base64,/, "")
      buffer = Buffer.from(base64Data, "base64")
    } else {
      const bytes = await image.arrayBuffer()
      buffer = Buffer.from(bytes)
    }

    const uploadsDir = join(process.cwd(), "src", "uploads")
    await fsPromises.mkdir(uploadsDir, { recursive: true })

    const filePath = join(uploadsDir, image.name)

    await fsPromises.writeFile(filePath, buffer)

    return NextResponse.json({ success: true, path: filePath })
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: "Erro ao processar o arquivo.",
    })
  }
}
