import isArray from "lodash/isArray"
import isString from "lodash/isString"
import i18n from "@/plugins/i18n"

const utils = {
  parseResponseError(err) {
    // process and return the relevant response message
    // :object err: error caught from response
    try {
      const response = err.response
      if (response.status === 400 && Object.keys(response).length) {
        let errors = response.data
        if (isArray(response.data) && response.data.length) {
          errors = response.data[0]
        }
        const firstError = Object.entries(errors)[0]
        if (isString(firstError[1])) {
          return `${firstError[0]} - ${firstError[1]}`
        }
        const nestedError = Object.entries(firstError[1])
        return `${firstError[0]} - ${nestedError[0]}`
      }
      return i18n.t("errors.genericError")
    } catch (err) {
      return i18n.t("errors.genericError")
    }
  },
}

export default utils
