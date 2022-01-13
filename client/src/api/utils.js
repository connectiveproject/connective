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
  parseUploadUsersFileError(err) {
    try {
      const response = err.response
      if (response.status === 400 && Object.keys(response).length) {
        let allErrorsArray = response.data
        let formattedErrorsArry = []
        // response include errors array. Go over each error line and format error message for each:
        for (const [i, rowErrorObj] of allErrorsArray.entries()) {
          // some errors are thrown from the file parser and include row numbers, and
          // some thrown from serializer/model and don't have row numbers:
          const rowIndex = "row" in rowErrorObj ? rowErrorObj.row : i + 1
          // we use negative row number for errors in file level (not row specific):
          const startMessage = rowIndex > 0 ? `${i18n.t("invite.uploadFileRowNumber")} ${rowIndex}: ` : ""
          let rowMessage
          if ("error" in rowErrorObj) {
            rowMessage = i18n.t(rowErrorObj.error) // parser error
          } else if ("profile" in rowErrorObj && "gender" in rowErrorObj.profile) {
            rowMessage = i18n.t("invite.genderError")
          } else {
            rowMessage = i18n.t("invite.unknownError")
          }
          formattedErrorsArry.push(`${startMessage} ${rowMessage}`)
        }
        // truncate the array to fit in screen size:
        formattedErrorsArry = formattedErrorsArry.slice(0, Math.min(formattedErrorsArry.length, 7))
        const formattedErrorStr = formattedErrorsArry.join("\n")
        return formattedErrorStr
      }
      return i18n.t("errors.genericError")
    } catch (err) {
      return i18n.t("errors.genericError")
    }
  },
}

export default utils
