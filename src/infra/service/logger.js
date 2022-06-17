import { get } from 'stack-trace'
import winston from 'winston'

const getFileName = () => {
  const boilerplateLines = (line) =>
    line &&
    line?.getFileName() &&
    line.getFileName().includes('src') &&
    !line.getFileName().includes('/node_modules/') &&
    !line.getFileName().includes('node:')

  try {
    const callSites = get().filter(boilerplateLines)

    if (callSites.length === 0) return 'Não encontrado'
    const results = new Set()
    for (const callSite of callSites) {
      results.add(callSite.getFileName())
    }
    if (results.size > 1) return Array.from(results)[1]
    return results.values().next().value
  } catch (e) {
    return 'Não encontrado'
  }
}

const humanReadableFormatter = ({ timestamp, level, message }) => {
  const fileName = getFileName().replace(/^.*src\//, 'src/')
  return `[${timestamp}] [${level}] [${fileName}] ${message}`
}

const logger = winston.createLogger({
  transports: [
    new winston.transports.Console({
      handleExceptions: true,
      humanReadableUnhandledException: true,
      stderrLevels: ['error', 'alert', 'critical', 'bizAlert'],
      format: winston.format.combine(
        winston.format.timestamp({ format: 'DD/MM/YYYY HH:mm:ss Z' }),
        winston.format.align(),
        winston.format.printf(humanReadableFormatter),
        winston.format.colorize({ all: true })
      ),
    }),
  ],
})

export default logger
