import { PrismaClient } from '@prisma/client'

export default class InputRepository {
  #prisma = new PrismaClient()
  async save(data) {
    const { lenguage, searchTerm, prefix, template, maxSentences } = data
    const newData = {
      lenguage,
      searchTerm,
      prefix,
      template,
      maxSentences,
    }
    const response = await this.#prisma.input.create({ data: newData })
    return response
  }

  async getById(id) {
    return this.#prisma.input.findFirst({
      where: {
        id,
      },
    })
  }

  async getInfoToVideoById(id) {
    const response = await this.#prisma.input.findFirst({
      where: {
        id,
      },
      select: {
        prefix: true,
        searchTerm: true,
        Text: {
          select: {
            origin: true,
            Sentences: {
              select: {
                sentence: true,
                keywords: true,
                image: {
                  select: {
                    url: true,
                  },
                  where: {
                    downloaded: true,
                  },
                },
              },
            },
          },
        },
      },
    })

    if (!response) throw new Error('Input não encontrado')
    return response
  }
}
