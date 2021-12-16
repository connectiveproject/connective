import isArray from "lodash/isArray"
import isString from "lodash/isString"
import i18n from "@/plugins/i18n"

const utils = {
  parseResponseError(err) {
    // process and return the relevant response message
    // :object/str err: error caught from response
    if (typeof (err) === "string") {
      return err
    }
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
  parseUploadConsumerFileError(err) {
    try {
      const response = err.response
      if (response.status === 400 && Object.keys(response).length) {
        let allErrorsArray = response.data
        const formattedErrorStr = allErrorsArray.map(errorObj => `${"row" in errorObj ? i18n.t("invite.uploadFileRowNumber") + " " + errorObj.row + ": " : ""}  ${i18n.t(errorObj.error)}`).join("\n")
        return formattedErrorStr
      }
      return i18n.t("errors.genericError")
    } catch (err) {
      return i18n.t("errors.genericError")
    }
  },
}

export default utils
