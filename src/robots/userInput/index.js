import { optionsLenguage, optionsTemplate } from './utils/constants.js'
import promptSync from 'prompt-sync'
import InputRepository from '../../repository/input.js'

export default class UserInput {
  #input = promptSync({ sigint: true })
  #inputRepository = new InputRepository()
  constructor(inputRepository = new InputRepository()) {
    this.#inputRepository = inputRepository
  }

  #askAndReturnLenguage() {
    console.log('Available languages:')
    for (const [key, value] of Object.entries(optionsLenguage)) {
      console.log(`${key} - ${value}`)
    }

    const lenguage = this.#input('Select a lenguage: ')
    if (!this.#validateValue(lenguage, optionsLenguage)) {
      console.log('Invalid lenguage')
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
      console.log('Invalid search term')
      throw new Error('The search term is empty')
    }
    return searchTerm
  }

  #askPrefix() {
    const prefix = this.#input('Enter a prefix: ')
    if (!prefix) {
      console.log('Invalid prefix')
      throw new Error('The prefix is empty')
    }
    return prefix
  }

  #getMaxSentence() {
    return 7
  }

  #askTemplate() {
    console.log('Available templates:')
    for (const [key, value] of Object.entries(optionsTemplate)) {
      console.log(`${key} - ${value}`)
    }
    const template = this.#input('Select a template: ')
    if (!this.#validateValue(template, optionsTemplate)) {
      console.log('Invalid template')
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
    const input = {}
    input.lenguage = this.#onlyInputValid(this.#askAndReturnLenguage.bind(this))
    input.searchTerm = this.#onlyInputValid(
      this.#askAndReturnSearchTerm.bind(this)
    )
    input.prefix = this.#onlyInputValid(this.#askPrefix.bind(this))
    input.template = this.#onlyInputValid(this.#askTemplate.bind(this))
    input.maxSentences = this.#getMaxSentence()

    console.log(input)
    try {
      const { id } = await this.#inputRepository.save(input)
      return id
    } catch (e) {
      console.log('Error saving input')
      console.log(e)
      throw e
    }
  }
}
