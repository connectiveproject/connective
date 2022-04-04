import i18n from "@/plugins/i18n"

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

export const GRADE_CHOICES = [
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

export const GENDER_CHOICES = [
  {
    text: i18n.t("genderFilters.boys"),
    value: "MALE",
  },
  {
    text: i18n.t("genderFilters.girls"),
    value: "FEMALE",
  },
]
