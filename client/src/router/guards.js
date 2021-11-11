import store from "@/vuex/store"
import { SERVER } from "@/helpers/constants/constants"
import { CAROUSEL_PLACEHOLDER } from "@/helpers/constants/images"

async function shouldCoordEditSchool() {
  // check if coord should edit school, by checking if other user already did
  const schoolDetails = await store.dispatch("school/getSchoolDetails")
  return !schoolDetails.lastUpdatedBy
}

/**
 * return a guard which runs the provided guards one-by-one. useful for Vue Router's `beforeEnter` function
 * @param {Function[]} guards - guards to run one after another.
 */
export function chainGuards(guards) {
  function runGuards(guards, from, to, finalNext, i) {
    let guard = guards[i]
    if (guards.length === i + 1) {
      // this is the last guard, exit
      return guard(from, to, finalNext)
    }
    guard(from, to, function (nextArg) {
      // this function replaces `next`, so we can use the argument provided after the guard ran to determine if it passed or failed
      // if it's empty (i.e., guard passed), we'll go over to the next guard. if not, the guard failed and we redirect to the failure route
      if (typeof nextArg === "undefined") {
        return runGuards(guards, from, to, finalNext, i + 1)
      }
      finalNext(nextArg)
    })
  }

  return function (from, to, next) {
    runGuards(guards, from, to, next, 0)
  }
}

export default {
  coordOnly(to, from, next) {
    if (store.getters["user/isCoordinator"]) {
      return next()
    }
    next("/")
  },
  vendorOnly(to, from, next) {
    if (store.getters["user/isVendor"]) {
      return next()
    }
    next("/")
  },
  consumerOnly(to, from, next) {
    if (store.getters["user/isConsumer"]) {
      return next()
    }
    next("/")
  },
  instructorOnly(to, from, next) {
    if (store.getters["user/isInstructor"]) {
      return next()
    }
    next("/")
  },
  supervisorOnly(to, from, next) {
    if (store.getters["user/isSupervisor"]) {
      return next()
    }
    next("/")
  },
  async checkRegistrationStatus(to, from, next) {
    // redirect based on user type & registration status
    const params = to.params
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
      return next({ name: "Dashboard", params: to.params })
    }
    next()
  },

  loginIfSignupComplete(to, from, next) {
    // login if finished registration process
    const isSignupComplete = store.state.user.userDetails.isSignupComplete
    if (isSignupComplete) {
      return next({ name: "Dashboard", params: to.params })
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
  segmentNotifyPage(to, from, next) {
    // https://github.com/segmentio/analytics-vue#-step-2-track-page-views-in-an-spa
    window.analytics.page(to.name)
    next()
  },
}
