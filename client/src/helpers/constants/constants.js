export const RECAPTCHA_SITE_KEY =
  process.env.VUE_APP_RECAPTCHA_SITE_KEY || "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
export const SERVER_URL = process.env.VUE_APP_BACKEND_URL
export const TERMS_OF_USE_URL = SERVER_URL.replace(
  "/api",
  "/terms_of_use_document"
)
export const LOGIN_API_URL = `${SERVER_URL}/auth/login/`
export const RESET_PASSWORD_URL = `${SERVER_URL}/auth/password-reset/confirm/`
export const CREATE_PASSWORD_RECOVERY_REQUEST_API_URL = `${SERVER_URL}/users/recover_password/`
export const UPDATE_TERMS_OF_USE_ACCEPTANCE_API_URL = `${SERVER_URL}/users/accept_terms_of_use/`
export const GET_TERMS_OF_USE_TEXT = `${SERVER_URL}/terms_of_use_docs/`
export const UPDATE_COORDINATOR_PROFILE_API_URL = `${SERVER_URL}/coordinators_profiles/`
export const UPDATE_CONSUMER_PROFILE_API_URL = `${SERVER_URL}/consumers_profiles/`
export const UPDATE_INSTRUCTOR_PROFILE_API_URL = `${SERVER_URL}/instructors_profiles/`
export const UPDATE_VENDOR_PROFILE_API_URL = `${SERVER_URL}/vendors_profiles/`
export const UPDATE_SUPERVISOR_PROFILE_API_URL = `${SERVER_URL}/supervisors_profiles/`
export const UPDATE_USER_API_URL = `${SERVER_URL}/users/`
export const GET_CONSUMER_PROFILE_API_URL = `${SERVER_URL}/consumers_profiles/me/`
export const GET_COORDINATOR_PROFILE_API_URL = `${SERVER_URL}/coordinators_profiles/me/`
export const GET_INSTRUCTOR_PROFILE_API_URL = `${SERVER_URL}/instructors_profiles/me/`
export const GET_VENDOR_PROFILE_API_URL = `${SERVER_URL}/vendors_profiles/me/`
export const GET_SUPERVISOR_PROFILE_API_URL = `${SERVER_URL}/supervisors_profiles/me/`
export const GET_USER_DETAILS_API_URL = `${SERVER_URL}/users/me/`
export const GET_SCHOOL_DETAILS_API_URL = `${SERVER_URL}/schools/me/`
export const UPDATE_SCHOOL_DETAILS_API_URL = `${SERVER_URL}/schools/`
export const GET_SCHOOL_LIST_API_URL = `${SERVER_URL}/schools/`
export const GET_SCHOOL_STUDENTS_LIST_API_URL = `${SERVER_URL}/manage_consumers/`
export const ADD_SCHOOL_STUDENTS_API_URL = `${SERVER_URL}/manage_consumers/`
export const EDIT_SCHOOL_STUDENTS_API_URL = `${SERVER_URL}/manage_consumers/`
export const DELETE_SCHOOL_STUDENTS_API_URL = `${SERVER_URL}/manage_consumers/`
export const ADD_SCHOOL_STUDENTS_BULK_API_URL = `${SERVER_URL}/manage_consumers/bulk_create/`
export const GET_SCHOOL_STUDENTS_EXPORT_FILE_API_URL = `${SERVER_URL}/export_consumer_list/`
export const ADD_SCHOOL_COORDINATORS_BULK_API_URL = `${SERVER_URL}/manage_coordinators/bulk_create/`
export const GET_SCHOOL_COORDINATORS_EXPORT_FILE_API_URL = `${SERVER_URL}/export_coordinator_list/`
export const GET_SCHOOL_COORDINATORS_LIST_API_URL = `${SERVER_URL}/manage_coordinators/`
export const ADD_SCHOOL_COORDINATORS_API_URL = `${SERVER_URL}/manage_coordinators/`
export const EDIT_SCHOOL_COORDINATORS_API_URL = `${SERVER_URL}/manage_coordinators/`
export const DELETE_SCHOOL_COORDINATORS_API_URL = `${SERVER_URL}/manage_coordinators/`
export const GET_MY_ORGANIZATION_LIST = `${SERVER_URL}/organizations/`
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
export const GET_VENDOR_PROGRAM_GROUPS_API_URL = `${SERVER_URL}/school_activity_group/`
export const UPDATE_PROGRAM_GROUP_CONSUMERS_API_URL = `${SERVER_URL}/school_activity_group/`
export const UPDATE_VENDOR_PROGRAM_GROUP_API_URL = `${SERVER_URL}/school_activity_group/`
export const GET_PROGRAM_GROUP_CONSUMERS_API_URL = `${SERVER_URL}/school_activity_group/group_consumers/`
export const GET_INSTRUCTOR_PROGRAM_GROUP_CONSUMERS_API_URL = `${SERVER_URL}/school_activity_group/group_consumers/`
export const GET_EVENT_LIST_API_URL = `${SERVER_URL}/events/`
export const DELETE_EVENT_API_URL = `${SERVER_URL}/events/`
export const CREATE_EVENT_ORDER_API_URL = `${SERVER_URL}/event_order/`
export const UPDATE_EVENT_ORDER_API_URL = `${SERVER_URL}/event_order/`
export const GET_CONSUMER_EVENT_LIST_API_URL = `${SERVER_URL}/consumer_events/`
export const GET_CONSUMER_EVENT_API_URL = `${SERVER_URL}/consumer_events/`
export const CREATE_CONSUMER_EVENT_FEEDBACK_API_URL = `${SERVER_URL}/consumer_event_feedback/`
export const GET_INSTRUCTOR_EVENT_LIST_API_URL = `${SERVER_URL}/events/`
export const GET_INSTRUCTOR_EVENT_API_URL = `${SERVER_URL}/events/`
export const UPDATE_INSTRUCTOR_EVENT_API_URL = `${SERVER_URL}/events/`
export const GET_VENDOR_EVENT_ORDERS_API_URL = `${SERVER_URL}/event_order/`
export const UPDATE_VENDOR_EVENT_ORDER_API_URL = `${SERVER_URL}/event_order/`
export const GET_EVENT_ORDERS_API_URL = `${SERVER_URL}/event_order/`
export const GET_VENDOR_EVENT_LIST_API_URL = `${SERVER_URL}/events/`
export const DELETE_EVENT_ORDER_API_URL = `${SERVER_URL}/event_order/`
export const CREATE_FEED_POST_API_URL = `${SERVER_URL}/posts/`
export const CREATE_POST_IMAGES_API_URL = `${SERVER_URL}/post_image/`
export const GET_TOP_CONSUMER_REQUESTS_STATS_API_URL = `${SERVER_URL}/school_activity_group/consumer_requests_data/`
export const GET_MY_NOTIFICATIONS = `${SERVER_URL}/my_notification/`
export const GET_HAS_NEW_NOTIFICATIONS = `${SERVER_URL}/my_notification/has_new/`
export const UPDATE_NOTIFICATION = `${SERVER_URL}/my_notification/`
export const UPDATE_NOTIFICATIONS_MARK_ALL_AS_READ = `${SERVER_URL}/my_notification/mark_all_as_read/`
export const GET_EVENT_EXPORT_FILE_API_URL = `${SERVER_URL}/export_events/`
export const GET_ALL_TAGS_API_URL = `${SERVER_URL}/tags/`

export const TOKEN_COOKIE_NAME = "token"
export const PASSWORD_REGEX_PATTERN =
  "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})"
export const ISRAELI_PHONE_REGEX_PATTERN =
  "^0(([23489]{1}\\d{7})|[57]{1}\\d{8})$"
export const EMAIL_REGEX_PATTERN =
  '^(([^<>()[\\]\\.,;:\\s@\\"]+(\\.[^<>()[\\]\\.,;:\\s@\\"]+)*)|(\\".+\\"))@(([^<>()[\\]\\.,;:\\s@\\"]+\\.)+[^<>()[\\]\\.,;:\\s@\\"]{2,})$'
export const WEBSITE_REGEX_PATTERN =
  "^(https?:\\/\\/)?" + // protocol
  "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
  "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
  "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
  "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
  "(\\#[-a-z\\d_]*)?$" // fragment locator

export const YOUTUBE_URL_REGEX_PATTERN =
  /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/
export const YOUTUBE_ID_REGEX_PATTERN =
  /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/

export const HEBREW_REGEX_PATTERN = /[\u0590-\u05FF]/
export const ARABIC_REGEX_PATTERN = /[\u0621-\u064A]/

export const ZIP_CODE_VALIDATION_RULE = "numeric|digits:7"

export const SCHOOL_GRADES_ITEMS = [
  { value: 1, textKey: "grades.1" },
  { value: 2, textKey: "grades.2" },
  { value: 3, textKey: "grades.3" },
  { value: 4, textKey: "grades.4" },
  { value: 5, textKey: "grades.5" },
  { value: 6, textKey: "grades.6" },
  { value: 7, textKey: "grades.7" },
  { value: 8, textKey: "grades.8" },
  { value: 9, textKey: "grades.9" },
  { value: 10, textKey: "grades.10" },
  { value: 11, textKey: "grades.11" },
  { value: 12, textKey: "grades.12" },
  { value: 13, textKey: "grades.13" },
  { value: 14, textKey: "grades.14" },
]

const DOMAIN_SELECT_ITEMS = [
  {
    textKey: "programFilters.scienceAndTech",
    value: "SCIENCE_AND_TECH",
  },
  {
    textKey: "programFilters.extremeSports",
    value: "EXTREME_SPORTS",
  },
  {
    textKey: "programFilters.field",
    value: "FIELD",
  },
  {
    textKey: "programFilters.other",
    value: "OTHER",
  },
]

export const VENDOR_PROGRAM_FIELDS = [
  {
    name: "name",
    labelKey: "program.programName",
    rules: "required|max:35",
  },
  {
    name: "description",
    labelKey: "program.programDescription",
    rules: "required|max:550",
    type: "textarea",
  },
  {
    name: "targetAudience",
    labelKey: "program.targetAudience",
    rules: "required",
    type: "select",
    choices: SCHOOL_GRADES_ITEMS,
    multiselect: true,
  },
  {
    name: "domain",
    labelKey: "program.domain",
    rules: "required",
    type: "select",
    choices: DOMAIN_SELECT_ITEMS,
    multiselect: false,
  },
  {
    name: "activityWebsiteUrl",
    labelKey: "general.website",
    rules: "website|max:750",
  },
  {
    name: "activityEmail",
    labelKey: "program.emailToGetInTouch",
    rules: "required|email",
  },
  {
    name: "contactName",
    labelKey: "program.contactName",
    rules: "required|max:60",
  },
  {
    name: "phoneNumber",
    labelKey: "general.phoneNumber",
    rules: "required|numeric|phoneNumberIsrael",
  },
  {
    name: "logo",
    labelKey: "program.logo",
    rules: "required|size:5000",
    type: "file",
    attrs: {
      appendIcon: "mdi-camera",
      prependIcon: null,
      accept: "image/*",
      clearable: true,
    },
    value: undefined,
  },
  {
    name: "tags",
    labelKey: "program.tagsLabel",
    type: "tags",
    rules: "",
  },
]

export const SERVER = {
  userTypes: {
    coordinator: "COORDINATOR", // i.e., principals
    consumer: "CONSUMER", // i.e., students
    instructor: "INSTRUCTOR", // i.e., guide
    vendor: "VENDOR", // i.e., organization managers
    supervisor: "SUPERVISOR",
  },
  programOrderStatus: {
    cancelled: "CANCELLED",
    pendingAdminApproval: "PENDING_ADMIN_APPROVAL",
    approved: "APPROVED",
    notOrdered: "NOT_ORDERED",
    denied: "DENIED",
  },
  programGroupTypes: {
    standard: "DEFAULT",
    containerOnly: "CONTAINER_ONLY",
    disabledConsumers: "DISABLED_CONSUMERS",
    noRegistration: "NO_REGISTRATION",
  },
  eventOrderStatus: {
    cancelled: "CANCELLED",
    pendingVendorApproval: "PENDING_APPROVAL",
    approved: "APPROVED",
    denied: "DENIED",
  },
  eventOrderReccurence: {
    oneTime: "ONE_TIME",
    weekly: "WEEKLY",
  },
  consumerProgramJoinStatus: {
    joined: "JOINED",
    notJoined: "NOT_JOINED",
    pendingGroupAssignment: "PENDING_GROUP_ASSIGNMENT",
  },
  domains: {
    scienceAndTech: "SCIENCE_AND_TECH",
    extremeSports: "EXTREME_SPORTS",
    field: "FIELD",
    other: "OTHER",
  },
  eventCancellationReasons: {
    illness: "ILLNESS",
    weather: "WEATHER",
    examSeason: "EXAM_SEASON",
    covid19: "COVID_19",
    holiday: "HOLIDAY",
    other: "OTHER",
  }
}

export const YOUTUBE_EMBED_URL = "https://www.youtube.com/embed/"
export const SEGMENT_EVENTS = {
  usersInvitedViaTable: "users_invited_via_table",
  usersInvitedViaImport: "users_invited_via_import",
  profileEdited: "profile_edited",
  programOpened: "program_opened",
  programJoined: "program_joined",
  warning: "warning",
}
export const LANGUAGE_TO_RTL = {
  "he": true,
}

export const VUEX_STATE = {
  notificationHasNew: "notification.hasNew"
}
