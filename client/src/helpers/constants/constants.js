import i18n from "../../plugins/i18n"

const SERVER_URL = process.env.VUE_APP_BACKEND_URL
export const LOGIN_API_URL = `${SERVER_URL}/auth/login/`
export const RESET_PASSWORD_URL = `${SERVER_URL}/auth/password-reset/confirm/`
export const UPDATE_COORDINATOR_PROFILE_API_URL = `${SERVER_URL}/coordinators_profiles/`
export const UPDATE_CONSUMER_PROFILE_API_URL = `${SERVER_URL}/consumers_profiles/`
export const UPDATE_INSTRUCTOR_PROFILE_API_URL = `${SERVER_URL}/instructors_profiles/`
export const UPDATE_VENDOR_PROFILE_API_URL = `${SERVER_URL}/vendors_profiles/`
export const UPDATE_USER_API_URL = `${SERVER_URL}/users/`
export const GET_CONSUMER_PROFILE_API_URL = `${SERVER_URL}/consumers_profiles/me/`
export const GET_COORDINATOR_PROFILE_API_URL = `${SERVER_URL}/coordinators_profiles/me/`
export const GET_INSTRUCTOR_PROFILE_API_URL = `${SERVER_URL}/instructors_profiles/me/`
export const GET_VENDOR_PROFILE_API_URL = `${SERVER_URL}/vendors_profiles/me/`
export const GET_USER_DETAILS_API_URL = `${SERVER_URL}/users/me/`
export const GET_SCHOOL_DETAILS_API_URL = `${SERVER_URL}/schools/me/`
export const UPDATE_SCHOOL_DETAILS_API_URL = `${SERVER_URL}/schools/`
export const GET_SCHOOL_STUDENTS_LIST_API_URL = `${SERVER_URL}/manage_consumers/`
export const ADD_SCHOOL_STUDENTS_API_URL = `${SERVER_URL}/manage_consumers/`
export const EDIT_SCHOOL_STUDENTS_API_URL = `${SERVER_URL}/manage_consumers/`
export const DELETE_SCHOOL_STUDENTS_API_URL = `${SERVER_URL}/manage_consumers/`
export const GET_SCHOOL_COORDINATORS_LIST_API_URL = `${SERVER_URL}/manage_coordinators/`
export const ADD_SCHOOL_COORDINATORS_API_URL = `${SERVER_URL}/manage_coordinators/`
export const EDIT_SCHOOL_COORDINATORS_API_URL = `${SERVER_URL}/manage_coordinators/`
export const DELETE_SCHOOL_COORDINATORS_API_URL = `${SERVER_URL}/manage_coordinators/`
export const GET_ORGANIZATION_INSTRUCTORS_LIST_API_URL = `${SERVER_URL}/manage_instructors/`
export const ADD_ORGANIZATION_INSTRUCTORS_API_URL = `${SERVER_URL}/manage_instructors/`
export const DELETE_ORGANIZATION_INSTRUCTORS_API_URL = `${SERVER_URL}/manage_instructors/`
export const EDIT_ORGANIZATION_INSTRUCTORS_API_URL = `${SERVER_URL}/manage_instructors/`
export const GET_ORGANIZATION_VENDORS_LIST_API_URL = `${SERVER_URL}/manage_vendors/`
export const ADD_ORGANIZATION_VENDORS_API_URL = `${SERVER_URL}/manage_vendors/`
export const DELETE_ORGANIZATION_VENDORS_API_URL = `${SERVER_URL}/manage_vendors/`
export const EDIT_ORGANIZATION_VENDORS_API_URL = `${SERVER_URL}/manage_vendors/`
export const GET_PROGRAM_LIST_API_URL = `${SERVER_URL}/activities/`
export const GET_CONSUMER_PROGRAM_LIST_API_URL = `${SERVER_URL}/consumer_activities/`
export const GET_VENDOR_PROGRAM_LIST_API_URL = `${SERVER_URL}/vendor_activities/`
export const CREATE_VENDOR_PROGRAM_API_URL = `${SERVER_URL}/vendor_activities/`
export const DELETE_VENDOR_PROGRAM_API_URL = `${SERVER_URL}/vendor_activities/`
export const UPDATE_VENDOR_PROGRAM_API_URL = `${SERVER_URL}/vendor_activities/`
export const GET_PROGRAM_MEDIA_LIST_API_URL = `${SERVER_URL}/activity_media/`
export const DELETE_PROGRAM_MEDIA_API_URL = `${SERVER_URL}/activity_media/`
export const CREATE_PROGRAM_MEDIA_API_URL = `${SERVER_URL}/activity_media/`
export const GET_SCHOOL_PROGRAM_ORDERS_LIST_API_URL = `${SERVER_URL}/manage_school_activity/`
export const ORDER_SCHOOL_PROGRAM_API_URL = `${SERVER_URL}/manage_school_activity/`
export const CONSUMER_JOIN_PROGRAM_API_URL = `${SERVER_URL}/consumer_activities/`
export const CONSUMER_LEAVE_PROGRAM_API_URL = `${SERVER_URL}/consumer_activities/`
export const GET_PROGRAM_GROUPS_API_URL = `${SERVER_URL}/school_activity_group/`
export const UPDATE_PROGRAM_GROUP_API_URL = `${SERVER_URL}/school_activity_group/`
export const CREATE_PROGRAM_GROUP_API_URL = `${SERVER_URL}/school_activity_group/`
export const DELETE_PROGRAM_GROUP_API_URL = `${SERVER_URL}/school_activity_group/`
export const GET_CONSUMER_PROGRAM_GROUPS_API_URL = `${SERVER_URL}/school_activity_group/`
export const UPDATE_PROGRAM_GROUP_CONSUMERS_API_URL = `${SERVER_URL}/school_activity_group/`
export const GET_PROGRAM_GROUP_CONSUMERS_API_URL = `${SERVER_URL}/school_activity_group/`
export const GET_INSTRUCTOR_PROGRAM_GROUP_CONSUMERS_API_URL = `${SERVER_URL}/school_activity_group/`
export const GET_EVENT_LIST_API_URL = `${SERVER_URL}/events/`
export const GET_CONSUMER_EVENT_LIST_API_URL = `${SERVER_URL}/consumer_events/`
export const GET_CONSUMER_EVENT_API_URL = `${SERVER_URL}/consumer_events/`
export const CREATE_CONSUMER_EVENT_FEEDBACK_API_URL = `${SERVER_URL}/consumer_event_feedback/`
export const GET_INSTRUCTOR_EVENT_LIST_API_URL = `${SERVER_URL}/events/`
export const GET_INSTRUCTOR_EVENT_API_URL = `${SERVER_URL}/events/`
export const UPDATE_INSTRUCTOR_EVENT_API_URL = `${SERVER_URL}/events/`
export const GET_TOP_CONSUMER_REQUESTS_STATS_API_URL = `${SERVER_URL}/school_activity_group/consumer_requests_data/`


export const TOKEN_COOKIE_NAME = "token"
export const PASSWORD_REGEX_PATTERN =
  "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})"
export const ISRAELI_PHONE_REGEX_PATTERN =
  "^0(([23489]{1}\\d{7})|[5]{1}\\d{8})$"
export const EMAIL_REGEX_PATTERN =
  '^(([^<>()[\\]\\.,;:\\s@\\"]+(\\.[^<>()[\\]\\.,;:\\s@\\"]+)*)|(\\".+\\"))@(([^<>()[\\]\\.,;:\\s@\\"]+\\.)+[^<>()[\\]\\.,;:\\s@\\"]{2,})$'
export const WEBSITE_REGEX_PATTERN =
  "^(https?:\\/\\/)" + // protocol
  "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
  "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
  "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
  "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
  "(\\#[-a-z\\d_]*)?$" // fragment locator

export const YOUTUBE_URL_REGEX_PATTERN =
  /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/
export const YOUTUBE_ID_REGEX_PATTERN =
  /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/
export const ZIP_CODE_VALIDATION_RULE = "numeric|digits:7"

export const SCHOOL_GRADES_ITEMS = [
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

const DOMAIN_SELECT_ITEMS = [
  {
    text: i18n.t("programFilters.scienceAndTech"),
    value: "SCIENCE_AND_TECH",
  },
  {
    text: i18n.t("programFilters.extremeSports"),
    value: "EXTREME_SPORTS",
  },
  {
    text: i18n.t("programFilters.field"),
    value: "FIELD",
  },
]

export const VENDOR_PROGRAM_FIELDS = [
  {
    name: "name",
    label: i18n.t("program.programName"),
    rules: "required|max:35",
  },
  {
    name: "description",
    label: i18n.t("program.programDescription"),
    rules: "required",
  },
  {
    name: "targetAudience",
    label: i18n.t("program.targetAudience"),
    rules: "required",
    type: "select",
    choices: SCHOOL_GRADES_ITEMS,
    multiselect: true,
  },
  {
    name: "domain",
    label: i18n.t("program.domain"),
    rules: "required",
    type: "select",
    choices: DOMAIN_SELECT_ITEMS,
    multiselect: false,
  },
  {
    name: "activityWebsiteUrl",
    label: i18n.t("general.website"),
    rules: "required|website",
  },
  {
    name: "activityEmail",
    label: i18n.t("general.email"),
    rules: "required|email",
  },
  {
    name: "contactName",
    label: i18n.t("program.contactName"),
    rules: "required",
  },
  {
    name: "phoneNumber",
    label: i18n.t("general.phoneNumber"),
    rules: "required|numeric|phoneNumberIsrael",
  },
]

export const CONSUMER_TAGS = [
  "פעילויות חוץ",
  "שפות זרות",
  "אתגר פיזי",
  "שחיה",
  "קהל דתי"
]

export const CONSUMER_PROGRAMS_CHECKBOX_FILTERS = [

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
]

export const PROGRAMS_CHECKBOX_FILTERS = [
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
    ],
  },
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
]

export const SERVER = {
  userTypes: {
    coordinator: "COORDINATOR", // i.e., principals
    consumer: "CONSUMER", // i.e., students
    instructor: "INSTRUCTOR", // i.e., guide
    vendor: "VENDOR", // i.e., organization managers
  },
  programOrderStatus: {
    cancelled: "CANCELLED",
    pendingAdminApproval: "PENDING_ADMIN_APPROVAL",
    approved: "APPROVED",
  },
  programGroupTypes: {
    standard: "DEFAULT",
    containerOnly: "CONTAINER_ONLY",
    disabledConsumers: "DISABLED_CONSUMERS",
  },
}

export const YOUTUBE_EMBED_URL = "https://www.youtube.com/embed/"
