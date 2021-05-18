import store from "../vuex/store.js"
import i18n from "../plugins/i18n"

async function isStaffRegistered() {
  // check if staff completed registration
  let profile = await store.dispatch("user/getProfile")
  let userDetails = await store.dispatch("user/getUserDetails")
  let schoolDetails = await store.dispatch("school/getSchoolDetails")
  return [
    profile.phoneNumber,
    userDetails.firstName,
    userDetails.lastName,
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
  const userType = userDetails.groups[0]
  if (userType === "students") {
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

export function flushPagination(to, from, next) {
  store.dispatch("pagination/flushState")
  next()
}

export function flushToken(to, from, next) {
  store.dispatch("auth/logout", false)
  next()
}
