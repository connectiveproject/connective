import store from "../vuex/store.js"
import i18n from "../plugins/i18n"
import { SERVER } from "../helpers/constants/constants"
import { CAROUSEL_PLACEHOLDER } from "../helpers/constants/images"

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
  const schoolDetails = await store.dispatch("school/getSchoolDetails")
  return schoolDetails.lastUpdatedBy
}

export async function checkRegistrationStatus(to, from, next) {
  // redirect based on user type & registration status
  if (!store.state.auth.isAuthenticated) {
    next("/")
    return
  }
  const userDetails = await store.dispatch("user/getUserDetails")
  if (userDetails.userType === SERVER.userTypes.consumer) {
    return next({ name: "StudentDashboard", params: { lang: i18n.locale } })
  } else if (userDetails.userType === SERVER.userTypes.instructor) {
    return next({ name: "InstructorDashboard", params: { lang: i18n.locale } })
  } else if (userDetails.userType === SERVER.userTypes.vendor) {
    if (await isStaffRegistered()) {
      return next({ name: "VendorDashboard", params: { lang: i18n.locale } })
    }
    return next({ name: "VendorRegister", params: { lang: i18n.locale } })
  }
  // coord
  const shouldEditSchool = !(await isSchoolFilled())
  if (!shouldEditSchool && (await isStaffRegistered())) {
    return next({ name: "MyGroups", params: { lang: i18n.locale } })
  }
  return next({
    name: "CoordinatorRegister",
    params: { lang: i18n.locale, shouldEditSchool },
  })
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
  await store.dispatch("program/getProgramsList", { usePagination: true })
  next()
}

export async function initConsumerPrograms(to, from, next) {
  // set pagination config & fetch initial program list from server
  store.dispatch("pagination/flushState")
  await store.dispatch("pagination/updatePagination", { itemsPerPage: 6 })
  await store.dispatch("consumerProgram/getProgramsList", {
    usePagination: true,
  })
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

export async function populateConsumerData(to, from, next) {
  await Promise.all([
    store.dispatch("user/getUserDetails"),
    store.dispatch("consumer/getProfile"),
  ])
  next()
}

export async function populateCoordinatorData(to, from, next) {
  await Promise.all([
    store.dispatch("school/getSchoolDetails"),
    store.dispatch("coordinator/getProfile"),
    store.dispatch("user/getUserDetails"),
  ])
  next()
}

export async function populateInstructorData(to, from, next) {
  await Promise.all([
    store.dispatch("instructor/getProfile"),
    store.dispatch("user/getUserDetails"),
  ])
  next()
}

export async function populateVendorData(to, from, next) {
  await Promise.all([
    store.dispatch("vendor/getProfile"),
    store.dispatch("user/getUserDetails"),
  ])
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
    mediaList = [{ imageUrl: CAROUSEL_PLACEHOLDER, mediaType: "image" }]
  }
  to.params.program = program
  to.params.mediaList = mediaList
  next()
}
