import fs from "fs"
import { NextResponse } from "next/server"
import { join } from "path"

export async function GET(request: Request) {
  try {
    const outDir = join(process.cwd(), "public", "outs")
    fs.unlink(`${outDir}/result.png`, (err) => {
      if (err) {
        return NextResponse.json({
          success: false,
          message: "Erro ao deletar o arquivo.",
        })
      }
    })

    return NextResponse.json({
      success: true,
      message: "Arquivo deletado com sucesso.",
    })
  } catch (error) {
    return NextResponse.json({
      success: false,
      message: "Erro ao processar o arquivo.",
    })
  }
}
