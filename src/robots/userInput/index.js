import promptSync from 'prompt-sync'

import logger from '../../infra/service/logger.js'
import InputRepository from '../../repository/input.js'
import { optionsLenguage, optionsTemplate } from './utils/constants.js'

export default class UserInput {
  #input = promptSync({ sigint: true })
  #inputRepository = new InputRepository()
  constructor(inputRepository = new InputRepository()) {
    this.#inputRepository = inputRepository
  }

  #askAndReturnLenguage() {
    logger.info('Linguas disponíveis:')
    const listLenguages = []
    for (const [key, value] of Object.entries(optionsLenguage)) {
      listLenguages.push(`${key} - ${value}`)
    }
    logger.info(listLenguages.join('\n'))

    const lenguage = this.#input('Select a lenguage: ')
    if (!this.#validateValue(lenguage, optionsLenguage)) {
      logger.error('Invalid lenguage')
      throw new Error(`The lenguage ${lenguage} is not available`)
    }
    return lenguage
  }

  #validateValue(value, options) {
    if (!options[value]) {
      return false
    }
    return true
  }

  #askAndReturnSearchTerm() {
    const searchTerm = this.#input('Enter a search term: ')
    if (!searchTerm) {
      logger.error('Invalid search term')
      throw new Error('The search term is empty')
    }
    return searchTerm
  }

  #askPrefix() {
    const prefix = this.#input('Enter a prefix: ')
    if (!prefix) {
      logger.error('Invalid prefix')
      throw new Error('The prefix is empty')
    }
    return prefix
  }

  #getMaxSentence() {
    return 7
  }

  #askTemplate() {
    logger.info('Templates disponíveis:')
    const listTemplates = []
    for (const [key, value] of Object.entries(optionsTemplate)) {
      listTemplates.push(`${key} - ${value}`)
    }
    logger.info(listTemplates.join('\n'))
    const template = this.#input('Select a template: ')
    if (!this.#validateValue(template, optionsTemplate)) {
      logger.error('Invalid template')
      throw new Error(`The template ${template} is not available`)
    }
    return template
  }

  #onlyInputValid(func) {
    let value
    do {
      try {
        value = func()
      } catch (e) {}
    } while (!value)
    return value
  }

  async run() {
    logger.info('Iniciando cadastro de input')
    const input = {}
    input.lenguage = this.#onlyInputValid(this.#askAndReturnLenguage.bind(this))
    input.searchTerm = this.#onlyInputValid(
      this.#askAndReturnSearchTerm.bind(this)
    )
    input.prefix = this.#onlyInputValid(this.#askPrefix.bind(this))
    input.template = this.#onlyInputValid(this.#askTemplate.bind(this))
    input.maxSentences = this.#getMaxSentence()

    const { id } = await this.#inputRepository.save(input)
    logger.info(`Input cadastrado com sucesso: ${id}`)
    return id
  }
}
