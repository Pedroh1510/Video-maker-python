import 'dotenv/config'
import path from 'node:path'

const CONFIG = {
  NLU_KEY: process.env.NLU_KEY,
  NLU_URL: process.env.NLU_URL,
  GOOGLE_SEARCH_API_KEY: process.env.GOOGLE_SEARCH_API_KEY,
  GOOGLE_SEARCH_ENGINE_ID: process.env.GOOGLE_SEARCH_ENGINE_ID,
  GOOGLE_CLIENT_SECRET_PATH: path.resolve(
    process.env.GOOGLE_CLIENT_SECRET_PATH
  ),
  GOOGLE_YOUTUBE_API_KEY: process.env.GOOGLE_YOUTUBE_API_KEY,
}

export default CONFIG
