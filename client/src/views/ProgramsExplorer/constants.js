import i18n from "../../plugins/i18n"

export const TAGS = [
  i18n.t("tags.outdoorActivities"),
  i18n.t("tags.foreignLanguages"),
  i18n.t("tags.physicalChallenge"),
  i18n.t("tags.swimming"),
  i18n.t("tags.suitedForReligious"),
]

export const PROGRAMS_CHECKBOX_FILTERS = [
  {
    name: "domain__in",
    readableName: i18n.t("programFilters.domainOfActivity"),
    options: [
      {
        label: i18n.t("programFilters.scienceAndTech"),
        value: "SCIENCE_AND_TECH",
      },
      {
        label: i18n.t("programFilters.extremeSports"),
        value: "EXTREME_SPORTS",
      },
      {
        label: i18n.t("programFilters.field"),
        value: "FIELD",
      },
      {
        label: i18n.t("programFilters.other"),
        value: "OTHER",
      },
    ],
  },
  {
    name: "targetAudience",
    readableName: i18n.t("programFilters.targetAudience"),
    options: [
      {
        label: i18n.t("grades.1"),
        value: "1",
      },
      {
        label: i18n.t("grades.2"),
        value: "2",
      },
      {
        label: i18n.t("grades.3"),
        value: "3",
      },
      {
        label: i18n.t("grades.4"),
        value: "4",
      },
      {
        label: i18n.t("grades.5"),
        value: "5",
      },
      {
        label: i18n.t("grades.6"),
        value: "6",
      },
      {
        label: i18n.t("grades.7"),
        value: "7",
      },
      {
        label: i18n.t("grades.8"),
        value: "8",
      },
      {
        label: i18n.t("grades.9"),
        value: "9",
      },
      {
        label: i18n.t("grades.10"),
        value: "10",
      },
      {
        label: i18n.t("grades.11"),
        value: "11",
      },
      {
        label: i18n.t("grades.12"),
        value: "12",
      },
    ],
  },
  // {
  //   name: "space",
  //   readableName: i18n.t("programFilters.space"),
  //   options: [
  //     {
  //       label: i18n.t("programFilters.blueCore"),
  //       value: "blue",
  //     },
  //     {
  //       label: i18n.t("programFilters.greenEmpowermentEnrichment"),
  //       value: "green",
  //     },
  //     {
  //       label: i18n.t("programFilters.orangeCommunity"),
  //       value: "orange",
  //     },
  //   ],
  // },
  // {
  //   name: "natureOfActivity",
  //   readableName: i18n.t("programFilters.natureOfActivity"),
  //   options: [
  //     {
  //       label: i18n.t("programFilters.individual"),
  //       value: "individual",
  //     },
  //     {
  //       label: i18n.t("programFilters.cooperative"),
  //       value: "cooperative",
  //     },
  //     {
  //       label: i18n.t("programFilters.hybrid"),
  //       value: "hybrid",
  //     },
  //   ],
  // },
]
