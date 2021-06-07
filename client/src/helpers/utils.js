import Papa from "papaparse"
import camelCase from "lodash/camelCase"
import isArray from "lodash/isArray"
import { YOUTUBE_ID_REGEX_PATTERN, YOUTUBE_EMBED_URL } from "./constants/constants"

const utils = {
  uploadedFileToUrl(file) {
    return window.URL.createObjectURL(file)
  },

  downloadTextAsFile(filename, content) {
    // :str filename: name to download by
    // :str content: file content
    let e = document.createElement("a")
    e.setAttribute(
      "href",
      "data:text/plain;charset=utf-8," + encodeURIComponent("\uFEFF" + content)
    )
    e.setAttribute("download", filename)
    document.body.appendChild(e)
    e.click()
    document.body.removeChild(e)
  },

  arrayToCsvFormat(arr) {
    return Papa.unparse(JSON.stringify(arr))
  },

  async csvToArray(csvFile) {
    let csvData = await csvFile.text()
    return Papa.parse(csvData, { header: true }).data
  },

  isNativeObject(obj) {
    // check if received parameter is a "simple" object
    return (
      obj instanceof Object && Object.getPrototypeOf(obj) === Object.prototype
    )
  },

  camelToSnakeCase(str) {
    return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
  },

  convertKeysCase(obj, convertCase) {
    // create a duplicate object with snake/camel case keys (recursively)
    // supports nested FormData, basic objects, arrays, primitive types
    // does not convert other objects, e.g., File
    // :str convertCase: case to convert to: 'camel' / 'snake'
    const convert =
      convertCase === "snake" ? this.camelToSnakeCase : camelCase
    if (obj instanceof FormData) {
      const convertedObj = new FormData()
      for (const [key, value] of obj.entries()) {
        convertedObj.append(
          convert(key),
          this.convertKeysCase(value, convertCase)
        )
      }
      return convertedObj
    } else if (isArray(obj)) {
      return obj.map(item => this.convertKeysCase(item, convertCase))
    } else if (this.isNativeObject(obj)) {
      const convertedObj = {}
      for (const [key, value] of Object.entries(obj)) {
        convertedObj[convert(key)] = this.convertKeysCase(value, convertCase)
      }
      return convertedObj
    }
    // no key found
    return obj
  },

  extractYoutubeVideoId(url) {
    const match = url.match(YOUTUBE_ID_REGEX_PATTERN)
    return match && match[2].length > 10 ? match[2] : null
  },

  youtubeToEmbeddedUrl(url) {
    // convert youtube url to an embedded url, to avoid 'X-Frame-Options' errors
    const vid = utils.extractYoutubeVideoId(url)
    if (vid) {
      return `${YOUTUBE_EMBED_URL}${vid}`
    }
    return url
  },
}

export default utils
