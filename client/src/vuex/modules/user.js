import Api from "@/api"
import { SERVER } from "@/helpers/constants/constants"

function getDefaultState() {
  return {
    userDetails: {
      slug: null,
      name: null,
      email: null,
      isSignupComplete: null,
      // e.g., COORDINATOR
      userType: null,
      superUser: false,
    },
  }
}

const user = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_USER_DETAILS(state, userDetails) {
      state.userDetails = userDetails
    },
    SET_USER_TYPE(state, userType) {
      state.userDetails.userType = userType
    },
    SET_SUPER_USER(state, superUser) {
      state.superUser = superUser
    }
  },
  getters: {
    isConsumer(state) {
      return state.userDetails.userType === SERVER.userTypes.consumer
    },
    isCoordinator(state) {
      return state.userDetails.userType === SERVER.userTypes.coordinator
    },
    isVendor(state) {
      return state.userDetails.userType === SERVER.userTypes.vendor
    },
    isInstructor(state) {
      return state.userDetails.userType === SERVER.userTypes.instructor
    },
    isSupervisor(state) {
      return state.userDetails.userType === SERVER.userTypes.supervisor
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getUserDetails({ commit, state }) {
      if (!state.userDetails.slug) {
        // fetch if not in cache
        let res = await Api.user.getUserDetails()
        commit("SET_USER_DETAILS", res.data)
      }
      window.analytics.identify(state.userDetails.slug, {
        name: state.userDetails.name,
        email: state.userDetails.email,
        user_type: state.userDetails.userType,
      })
      return state.userDetails
    },
    async updateUserDetails({ commit, state }, { slug, userDetails }) {
      let res = await Api.user.updateUserDetails(slug, userDetails)
      commit("SET_USER_DETAILS", res.data)
      return state.userDetails
    },
    updateUserType({ commit, state }, { userType }) {
      commit("SET_USER_TYPE", userType)
      return state.userType
    },
    async updateSuperUser({ commit, state }, { superUser }) {
      commit("SET_SUPER_USER", superUser)
      return state.superUser
    },

  },
}

export default user
