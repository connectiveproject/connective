import store from "@/vuex/store"
import i18n from "@/plugins/i18n"
import { SERVER } from "@/helpers/constants/constants"
import { CAROUSEL_PLACEHOLDER } from "@/helpers/constants/images"

async function shouldCoordEditSchool() {
  // check if coord should edit school, by checking if other user already did
  const schoolDetails = await store.dispatch("school/getSchoolDetails")
  return !schoolDetails.lastUpdatedBy
}

export default {
  async checkRegistrationStatus(to, from, next) {
    // redirect based on user type & registration status
    const params = { lang: i18n.locale }
    const isSignupComplete = store.state.user.userDetails.isSignupComplete
    const userToRoute = {
      [SERVER.userTypes.supervisor]: () =>
        next({ name: "SupervisorDashboard", params }),

      [SERVER.userTypes.consumer]: () =>
        next({ name: "StudentDashboard", params }),

      [SERVER.userTypes.instructor]: () =>
        next({ name: "InstructorDashboard", params }),

      [SERVER.userTypes.vendor]: async () => {
        if (isSignupComplete) {
          return next({ name: "VendorDashboard", params })
        }
        next({ name: "VendorRegister", params })
      },

      [SERVER.userTypes.coordinator]: async () => {
        if (isSignupComplete) {
          return next({ name: "MyGroups", params })
        }
        const shouldEditSchool = await shouldCoordEditSchool()
        return next({
          name: "CoordinatorRegister",
          params: { ...params, shouldEditSchool },
        })
      },
    }

    if (!store.state.auth.isAuthenticated) {
      return next("/")
    }
    const userDetails = await store.dispatch("user/getUserDetails")
    userToRoute[userDetails.userType]()
  },

  loginIfAuthenticated(to, from, next) {
    if (store.state.auth.isAuthenticated) {
      return next({ name: "Dashboard", params: { lang: i18n.locale } })
    }
    next()
  },

  loginIfSignupComplete(to, from, next) {
    // login if finished registration process
    const isSignupComplete = store.state.user.userDetails.isSignupComplete
    if (isSignupComplete) {
      return next({ name: "Dashboard", params: { lang: i18n.locale } })
    }
    if (isSignupComplete === null) {
      // if unknown, redirect to login page
      return next("/")
    }
    next()
  },

  async initPrograms(to, from, next) {
    // set pagination config & fetch initial program list from server
    store.dispatch("pagination/flushState")
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 6 })
    await store.dispatch("program/getProgramsList", { usePagination: true })
    next()
  },

  async initConsumerPrograms(to, from, next) {
    // set pagination config & fetch initial program list from server
    store.dispatch("pagination/flushState")
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 6 })
    await store.dispatch("consumerProgram/getProgramsList", {
      usePagination: true,
    })
    next()
  },

  async flushPagination(to, from, next) {
    await store.dispatch("pagination/flushState")
    next()
  },

  async populateConsumerData(to, from, next) {
    await Promise.all([
      store.dispatch("user/getUserDetails"),
      store.dispatch("consumer/getProfile"),
    ])
    next()
  },

  async populateCoordinatorData(to, from, next) {
    await Promise.all([
      store.dispatch("school/getSchoolDetails"),
      store.dispatch("coordinator/getProfile"),
      store.dispatch("user/getUserDetails"),
    ])
    next()
  },

  async populateInstructorData(to, from, next) {
    await Promise.all([
      store.dispatch("instructor/getProfile"),
      store.dispatch("user/getUserDetails"),
    ])
    next()
  },

  async populateVendorData(to, from, next) {
    await Promise.all([
      store.dispatch("vendor/getProfile"),
      store.dispatch("user/getUserDetails"),
    ])
    next()
  },

  async populateSupervisorData(to, from, next) {
    await Promise.all([
      store.dispatch("supervisor/getProfile"),
      store.dispatch("user/getUserDetails"),
    ])
    next()
  },

  async fetchProgramDetails(to, from, next) {
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
  },
}
