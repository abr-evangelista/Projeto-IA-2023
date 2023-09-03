import { FileType } from "@/app/recognize/page"
import { promises as fsPromises } from "fs"
import { NextResponse } from "next/server"
import { join } from "path"

export async function POST(request: Request) {
  try {
    const formData = await request.formData()

    const file: FileType = formData.get("file") as unknown as FileType
    const photoSrc: string = formData.get("photoSrc") as unknown as string

    if (!file) {
      return NextResponse.json({
        success: false,
        error: "Nenhum arquivo foi enviado.",
      })
    }

    let buffer: Buffer

    if (!!photoSrc) {
      const base64Data = photoSrc.replace(/^data:image\/\w+;base64,/, "")
      buffer = Buffer.from(base64Data, "base64")
    } else {
      const bytes = await file.arrayBuffer()
      buffer = Buffer.from(bytes)
    }

    const uploadsDir = join(process.cwd(), "src", "uploads")
    await fsPromises.mkdir(uploadsDir, { recursive: true })

    const filePath = join(uploadsDir, file.name)

    await fsPromises.writeFile(filePath, buffer)

    return NextResponse.json({ success: true, path: filePath })
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: "Erro ao processar o arquivo.",
    })
  }
}
