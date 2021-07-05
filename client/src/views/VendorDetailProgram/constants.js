import i18n from "../../plugins/i18n"

const targetAudienceSelectItems = [
  {
    text: i18n.t("grades.1"),
    value: 1,
  },
  {
    text: i18n.t("grades.2"),
    value: 2,
  },
  {
    text: i18n.t("grades.3"),
    value: 3,
  },
  {
    text: i18n.t("grades.4"),
    value: 4,
  },
  {
    text: i18n.t("grades.5"),
    value: 5,
  },
  {
    text: i18n.t("grades.6"),
    value: 6,
  },
  {
    text: i18n.t("grades.7"),
    value: 7,
  },
  {
    text: i18n.t("grades.8"),
    value: 8,
  },
  {
    text: i18n.t("grades.9"),
    value: 9,
  },
  {
    text: i18n.t("grades.10"),
    value: 10,
  },
  {
    text: i18n.t("grades.11"),
    value: 11,
  },
  {
    text: i18n.t("grades.12"),
    value: 12,
  },
]

const domainSelectItems = [
  {
    text: i18n.t("programFilters.scienceAndTech"),
    value: "scienceAndTech",
  },
  {
    text: i18n.t("programFilters.extremeSports"),
    value: "extremeSports",
  },
  {
    text: i18n.t("programFilters.field"),
    value: "field",
  },
]

export const programFields = [
  {
    name: "name",
    descriptiveName: i18n.t("program.programName"),
    validationRules: "required",
  },
  {
    name: "description",
    descriptiveName: i18n.t("program.programDescription"),
    validationRules: "required",
  },
  {
    name: "targetAudience",
    descriptiveName: i18n.t("program.targetAudience"),
    validationRules: "required",
    inputType: "select",
    selectItems: targetAudienceSelectItems,
    multiselect: true,
  },
  {
    name: "domain",
    descriptiveName: i18n.t("program.domain"),
    validationRules: "required",
    inputType: "select",
    selectItems: domainSelectItems,
    multiselect: false,
  },
  {
    name: "activityWebsiteUrl",
    descriptiveName: i18n.t("general.website"),
    validationRules: "required|website",
  },
  {
    name: "activityEmail",
    descriptiveName: i18n.t("general.email"),
    validationRules: "required|email",
  },
  {
    name: "contactName",
    descriptiveName: i18n.t("program.contactName"),
    validationRules: "required",
  },
  {
    name: "phoneNumber",
    descriptiveName: i18n.t("general.phoneNumber"),
    validationRules: "required|numeric|phoneNumberIsrael",
  },
]
