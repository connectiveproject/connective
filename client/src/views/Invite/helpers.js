import Utils from "../../helpers/utils"

export function exportCSV(studentsArray) {
  let csvData = Utils.arrayToCsvFormat(studentsArray)
  Utils.downloadTextAsFile("invitations.csv", csvData)
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
