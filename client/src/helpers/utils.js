import moment from "moment"
import Papa from "papaparse"
import camelCase from "lodash/camelCase"
import isArray from "lodash/isArray"
import {
  YOUTUBE_ID_REGEX_PATTERN,
  YOUTUBE_EMBED_URL,
} from "./constants/constants"

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
    if (str.toUpperCase() === str) {
      return str
    }
    return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
  },

  convertKeysCase(obj, convertCase) {
    // create a duplicate object with snake/camel case keys (recursively)
    // supports nested FormData, basic objects, arrays, primitive types
    // does not convert other objects, e.g., File
    // :str convertCase: case to convert to: 'camel' / 'snake'
    const convert = convertCase === "snake" ? this.camelToSnakeCase : camelCase
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

  dateBenchmarkToRange(benchmarkDate, daysRadius) {
    // recieve a moment.js date object and return two dates - before and after the original
    // :momentObject benchmarkDate
    // :Number daysRadius: number of days to move from each side
    const startDate = benchmarkDate.clone()
    const endDate = benchmarkDate.clone()
    startDate.subtract(daysRadius, "days")
    endDate.add(daysRadius, "days")
    return [startDate, endDate]
  },

  addDaysToToday(days) {
    // return a moment date object adding days to current date
    // :Int days: days to add, can be minus to subtract (doesn't support floats)
    const date = moment()
    date.add(days, "days")
    return date
  },

  dateToApiString(date) {
    // convert moment.js date object into a valid string to send to api
    return date.format("YYYY-MM-DD HH:mm")
  },

  ApiStringToReadableDate(dateString) {
    return moment(dateString).format("DD.MM.YYYY HH:mm")
  },

  stringToPsuedoRandomColor(str) {
    // return a "random" color based on the first two characters
    // it is useful when want to be color consistent, yet looking random
    const colors = [
      "blue",
      "indigo",
      "cyan",
      "deep-purple",
      "green",
      "orange",
      "grey darken-1",
    ]

    if (str.length <= 1) {
      return colors[1]
    }

    const colorPos = (str.charCodeAt(0) + str.charCodeAt(1)) % colors.length
    return colors[colorPos]
  },

  objectToFormData(obj) {
    const fd = new FormData()
    for (const [key, value] of Object.entries(obj)) {
      if (isArray(value)) {
        fd.append(key, JSON.stringify(value))
      } else {
        fd.append(key, value)
      }
    }
    return fd
  },
}

export default utils
