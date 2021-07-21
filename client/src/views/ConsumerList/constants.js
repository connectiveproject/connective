import i18n from "../../plugins/i18n"

export const CONSUMER_LIST_CHECKBOX_FILTERS = [
  {
    name: "gender",
    readableName: i18n.t("gender.gender"),
    options: [
      {
        label: i18n.t("gender.male"),
        value: "MALE",
      },
      {
        label: i18n.t("gender.female"),
        value: "FEMALE",
      },
      {
        label: i18n.t("gender.unknown"),
        value: "UNKNOWN",
      },
      {
        label: i18n.t("gender.other"),
        value: "OTHER",
      },
    ],
  },
]
