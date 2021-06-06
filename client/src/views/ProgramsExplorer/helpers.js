import i18n from "../../plugins/i18n"

export function getSubtitle(isConsumer) {
  if (isConsumer) {
    return i18n.t("program.searchAndFindTheProgramsYouLike!")
  }
  return i18n.t(
    "program.findForProgramsThatFitTheSchoolPedagogicalApproachAndStartCollaborating!"
  )
}
