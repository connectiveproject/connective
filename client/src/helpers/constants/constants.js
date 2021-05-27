import i18n from "../../plugins/i18n"

const serverUrl = `${window.location.origin.replace("8080", "8000")}/api` // todo replace with env variable
export const loginApiUrl = `${serverUrl}/auth/login/`
export const resetPasswordUrl = `${serverUrl}/auth/password-reset/confirm/`
export const updateCoordinatorProfileApiUrl = `${serverUrl}/coordinators_profiles/`
export const updateUserApiUrl = `${serverUrl}/users/`
export const getCoordinatorProfileApiUrl = `${serverUrl}/coordinators_profiles/me/`
export const getUserDetailsApiUrl = `${serverUrl}/users/me/`
export const getSchoolDetailsApiUrl = `${serverUrl}/schools/me`
export const updateSchoolDetailsApiUrl = `${serverUrl}/schools/`
export const getSchoolStudentListApiUrl = `${serverUrl}/manage_students/`
export const addSchoolStudentsApiUrl = `${serverUrl}/manage_students/`
export const editSchoolStudentsApiUrl = `${serverUrl}/manage_students/`
export const deleteSchoolStudentsApiUrl = `${serverUrl}/manage_students/`
export const getProgramsListApiUrl = `${serverUrl}/activities/`
export const getProgramMediaListApiUrl = `${serverUrl}/activity_media/`

export const tokenCookieName = "token"
export const schoolGradesItems = [
  { value: 1, text: i18n.t("grades.1") },
  { value: 2, text: i18n.t("grades.2") },
  { value: 3, text: i18n.t("grades.3") },
  { value: 4, text: i18n.t("grades.4") },
  { value: 5, text: i18n.t("grades.5") },
  { value: 6, text: i18n.t("grades.6") },
  { value: 7, text: i18n.t("grades.7") },
  { value: 8, text: i18n.t("grades.8") },
  { value: 9, text: i18n.t("grades.9") },
  { value: 10, text: i18n.t("grades.10") },
  { value: 11, text: i18n.t("grades.11") },
  { value: 12, text: i18n.t("grades.12") },
]

export const passwordRegexPattern =
  "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})"
export const israeliPhoneRegexPattern = "^0(([23489]{1}\\d{7})|[5]{1}\\d{8})$"
export const emailRegexPattern =
  '^(([^<>()[\\]\\.,;:\\s@\\"]+(\\.[^<>()[\\]\\.,;:\\s@\\"]+)*)|(\\".+\\"))@(([^<>()[\\]\\.,;:\\s@\\"]+\\.)+[^<>()[\\]\\.,;:\\s@\\"]{2,})$'
export const websiteRegexPattern =
  /[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)?/gi
export const youtubeIdRegexPattern =
  /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
export const zipCodeValidationRule = "required|numeric|digits:7"
export const programsCheckboxFilters = [
  {
    name: "space",
    readableName: i18n.t("programFilters.space"),
    options: [
      {
        label: i18n.t("programFilters.blueCore"),
        value: "blue",
      },
      {
        label: i18n.t("programFilters.greenEmpowermentEnrichment"),
        value: "green",
      },
      {
        label: i18n.t("programFilters.orangeCommunity"),
        value: "orange",
      },
    ],
  },
  {
    name: "domainOfActivity",
    readableName: i18n.t("programFilters.domainOfActivity"),
    options: [
      {
        label: i18n.t("programFilters.scienceAndTech"),
        value: "scienceAndTech",
      },
      {
        label: i18n.t("programFilters.extremeSports"),
        value: "extremeSports",
      },
      {
        label: i18n.t("programFilters.field"),
        value: "field",
      },
    ],
  },
  {
    name: "natureOfActivity",
    readableName: i18n.t("programFilters.natureOfActivity"),
    options: [
      {
        label: i18n.t("programFilters.individual"),
        value: "individual",
      },
      {
        label: i18n.t("programFilters.cooperative"),
        value: "cooperative",
      },
      {
        label: i18n.t("programFilters.hybrid"),
        value: "hybrid",
      },
    ],
  },
  {
    name: "targetAudience",
    readableName: i18n.t("programFilters.targetAudience"),
    options: [
      {
        label: i18n.t("programFilters.allAges"),
        value: "0",
      },
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
]

export const server = {
  userTypes: {
    coordinators: "coordinators", // i.e., principals
    consumers: "consumers", // i.e., students
    vendors: "vendors", // i.e., organization managers
  },
}

export const youtubeEmbedUrl = "https://www.youtube.com/embed/"
