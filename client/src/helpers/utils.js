import Compressor from "compressorjs"
import moment from "moment"
import Papa from "papaparse"
import camelCase from "lodash/camelCase"
import isArray from "lodash/isArray"
import cloneDeep from "lodash/cloneDeep"
import store from "@/vuex/store"


import {
  YOUTUBE_ID_REGEX_PATTERN,
  YOUTUBE_EMBED_URL,
  LANGUAGE_TO_RTL,
  VENDOR_PROGRAM_FIELDS,
} from "@/helpers/constants/constants"
import i18n from "@/plugins/i18n"

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
    // convert moment.js date object into a valid string in UTC timezone, to send to api
    const utcFormat = moment(date).utc().format("YYYY-MM-DD HH:mm")
    return utcFormat
  },

  ApiStringToReadableDate(dateString) {
    const dateFormat = store.state.vxPreferences.parameters.dateFormat
    const timeFormat = store.state.vxPreferences.parameters.timeFormat
    return moment(dateString).format(`${dateFormat} ${timeFormat}`)
  },

  apiStringToReadableDateNoTime(dateString) {
    const dateFormat = store.state.vxPreferences.parameters.dateFormat
    return moment(dateString).format(dateFormat)
  },
  apiStringToReadableTime(dateString) {
    const timeFormat = store.state.vxPreferences.parameters.timeFormat
    return moment(dateString).format(timeFormat)
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

  addWebsiteScheme(website) {
    // add https scheme to website
    if (!website) {
      return ""
    }
    if (website.toLowerCase().startsWith("http")) {
      return website
    }
    return `http://${website}`
  },

  async compressImageFile(img, quality = 0.8) {
    const compressed = await new Promise((resolve, reject) => {
      new Compressor(img, {
        quality,
        success: resolve,
        error: reject,
      })
    })
    // convert blob to file if needed
    return new File([compressed], compressed.name)
  },
  /**
  * Returns true if current language is RTL, false otherwise
  */
  checkRtl() {
    return LANGUAGE_TO_RTL[i18n.locale]
  },
  /**
  * dynamic translate and return vendor program fields
  */
  getVendorProgramFields() {
    const vendorProgramFields = cloneDeep(VENDOR_PROGRAM_FIELDS)
    for (const field of vendorProgramFields) {
      field.label = i18n.t(field.labelKey)
      if (field.choices) {
        field.choices = field.choices.map(item => ({
          text: i18n.t(item.textKey),
          value: item.value,
        }))
      }
    }
    return vendorProgramFields
  },
  getKeyByValue(obj, value) {
    return Object.keys(obj).find(key => obj[key] === value)
  },
  hasPrivilege(privilege) {
    return store.state.user.userDetails.privileges && store.state.user.userDetails.privileges.includes(privilege)
  }
}

export default utils
