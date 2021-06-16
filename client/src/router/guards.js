import store from "../vuex/store.js"
import i18n from "../plugins/i18n"
import { SERVER } from "../helpers/constants/constants"
import { PROGRAM_MEDIA_PLACEHOLDER } from "../helpers/constants/images"

async function isStaffRegistered() {
  // check if staff completed registration
  let userDetails = await store.dispatch("user/getUserDetails")
  let profile = await store.dispatch(
    `${userDetails.userType.toLowerCase()}/getProfile`
  )
  let schoolDetails = await store.dispatch("school/getSchoolDetails")
  return [
    profile.phoneNumber,
    userDetails.name,
    schoolDetails.contactPhone,
  ].every(item => !!item)
}

export async function checkRegistrationStatus(to, from, next) {
  // redirect based on user type & registration status
  // if not authenticated -> home screen
  // elif registration info missing -> registration page
  // else -> continue to relevant dashboard
  if (!store.state.auth.isAuthenticated) {
    next("/")
    return
  }
  // on server - need to add userType field
  const userDetails = await store.dispatch("user/getUserDetails")
  if (userDetails.userType === SERVER.userTypes.consumer) {
    next({ name: "StudentDashboard", params: { lang: i18n.locale } })
  } else if (await isStaffRegistered()) {
    next({ name: "ManagementDashboard", params: { lang: i18n.locale } })
  } else {
    next({ name: "Register", params: { lang: i18n.locale } })
  }
}

export function loginOrFlushStore(to, from, next) {
  // if logged in already, redirect to dashboard
  // else flush state (relevant on logouts)
  if (store.state.auth.isAuthenticated) {
    next({ name: "Dashboard", params: { lang: i18n.locale } })
  } else {
    store.dispatch("flushState")
    next()
  }
}

export async function initPrograms(to, from, next) {
  // set pagination config & fetch initial program list from server
  store.dispatch("pagination/flushState")
  await store.dispatch("pagination/updatePagination", { itemsPerPage: 6 })
  await store.dispatch("program/getProgramsList")
  next()
}

export async function initConsumerPrograms(to, from, next) {
  // set pagination config & fetch initial program list from server
  store.dispatch("pagination/flushState")
  await store.dispatch("pagination/updatePagination", { itemsPerPage: 6 })
  await store.dispatch("consumerProgram/getProgramsList")
  next()
}

export function flushPagination(to, from, next) {
  store.dispatch("pagination/flushState")
  next()
}

export function flushToken(to, from, next) {
  store.dispatch("auth/logout", false)
  next()
}

export function PopulateConsumerData(to, from, next) {
  store.dispatch("user/getUserDetails")
  store.dispatch("consumer/getProfile")
  next()
}

export function PopulateCoordinatorData(to, from, next) {
  store.dispatch("school/getSchoolDetails")
  next()
}

export async function fetchProgramDetails(to, from, next) {
  let vuexModule = "program"
  if (store.getters["user/isConsumer"]) {
    vuexModule = "consumerProgram"
  }
  let [program, mediaList] = await Promise.all([
    store.dispatch(`${vuexModule}/getProgram`, to.params.slug),
    store.dispatch(`${vuexModule}/getProgramMediaList`, to.params.slug),
  ])
  if (!mediaList.length) {
    mediaList = [{ imageUrl: PROGRAM_MEDIA_PLACEHOLDER, mediaType: "image" }]
  }
  to.params.program = program
  to.params.mediaList = mediaList
  next()
}
