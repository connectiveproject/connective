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
  return [profile.phoneNumber, userDetails.name].every(item => !!item)
}

async function isSchoolFilled() {
  // check if school details already filled by a coordinator
  let schoolDetails = await store.dispatch("school/getSchoolDetails")
  return schoolDetails.lastUpdatedBy
}

export async function checkRegistrationStatus(to, from, next) {
  // redirect based on user type & registration status
  if (!store.state.auth.isAuthenticated) {
    next("/")
    return
  }
  const userDetails = await store.dispatch("user/getUserDetails")
  switch (userDetails.userType) {
    case SERVER.userTypes.consumer:
      next({ name: "StudentDashboard", params: { lang: i18n.locale } })
      break
    case SERVER.userTypes.instructor:
      next({ name: "InstructorDashboard", params: { lang: i18n.locale } })
      break
    case SERVER.userTypes.vendor:
      if (await isStaffRegistered()) {
        next({ name: "VendorDashboard", params: { lang: i18n.locale } })
      } else {
        next({ name: "VendorRegister", params: { lang: i18n.locale } })
      }
      break
    case SERVER.userTypes.supervisor:
      next({ name: "SupervisorDashboard", params: { lang: i18n.locale } })
      break
    default:
      // coordinator
      if (await isStaffRegistered()) {
        next({ name: "CoordinatorDashboard", params: { lang: i18n.locale } })
      } else {
        const shouldEditSchool = !(await isSchoolFilled())
        next({
          name: "CoordinatorRegister",
          params: { lang: i18n.locale, shouldEditSchool },
        })
      }
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
