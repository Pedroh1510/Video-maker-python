import { IamAuthenticator } from 'ibm-watson/auth/index.js'
import Nltk from 'ibm-watson/natural-language-understanding/v1.js'

import CONFIG from '../config/env.js'

export default class Watson {
  nlu = new Nltk({
    version: '2021-10-15',
    authenticator: new IamAuthenticator({
      apikey: CONFIG.NLU_KEY,
    }),
    url: CONFIG.NLU_URL,
  })

  async nluAnalize(text, lenguage = 'en') {
    const response = await this.nlu.analyze({
      text,
      language: lenguage,
      clean: true,
      features: {
        keywords: {},
        entities: {},
        classifications: {},
        syntax: {
          sentences: true,
        },
        sentiment: {
          document: true,
        },
      },
    })
    if (!response?.result) throw new Error('No response from Watson')
    return {
      keywords: response.result.keywords,
      entities: response.result.entities,
      classifications: response.result.categories,
      sentences: response.result?.syntax?.sentences,
      tokens: response.result.syntax?.tokens,
      sentiment: response.result.sentiment,
    }
  }
}
