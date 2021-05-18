import i18n from "../../plugins/i18n"
import Utils from "../../helpers/utils"
import {
  israeliPhoneRegexPattern,
  emailRegexPattern,
} from "../../helpers/constants/constants"

export function exportCSV(studentsArray) {
  let csvData = Utils.arrayToCsvFormat(studentsArray)
  Utils.downloadTextAsFile("invitations.csv", csvData)
}

export function validateStudentsArray(arr) {
  // validate students array
  // return empty string on success, error string on error
  let obj = arr[0]
  if (
    !obj.identityNumber ||
    !obj.firstName ||
    !obj.city ||
    !obj.phoneNumber ||
    !obj.email
  ) {
    return i18n.t("errors.missingColumnsOrValues")
  }
  for (let student of arr) {
    if (!new RegExp(israeliPhoneRegexPattern).test(student.phoneNumber)) {
      return `${i18n.t("errors.invalidPhoneNumber")} - ${student.phoneNumber}`
    }
    if (!new RegExp(emailRegexPattern).test(student.email)) {
      return `${i18n.t("errors.invalidEmail")} ${student.email}`
    }
  }
  return ""
}

export function translateStatus(status) {
  switch (status) {
    case "pending_request_accept":
      return this.$t("invite.pendingRecipientApproval")
    case "registered":
      return this.$t("auth.registrationSucceeded")
  }
  return status
}
