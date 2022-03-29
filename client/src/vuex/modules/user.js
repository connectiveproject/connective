import Api from "@/api"
import { SERVER } from "@/helpers/constants/constants"

const SUPER_USER_TYPE = "GATEKEEPER"

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
    profile: {
      phoneNumber: null,
      profilePicture: null,
      jobDescription: null,
    },
    impersonateUserType: false,
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
    },
    SET_PROFILE(state, userProfile) {
      state.profile = userProfile
    },
    SET_IMPERSONATE_USER_TYPE(state, impersonateUserType) {
      state.impersonateUserType = impersonateUserType
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
    isImpersonateUserType(state) {
      return state.impersonateUserType
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
        if (state.userDetails.userType === SUPER_USER_TYPE) {
          commit("SET_SUPER_USER", true)
        }
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
      commit("SET_IMPERSONATE_USER_TYPE", state.superUser && userType !== SUPER_USER_TYPE)
      return state.userType
    },
    async updateSuperUser({ commit, state }, { superUser }) {
      commit("SET_SUPER_USER", superUser)
      return state.superUser
    },
    async getProfile({ commit, state }) {
      if (!state.profile.phoneNumber) {
        // fetch if not in cache
        let res = await Api.user.getProfile()
        commit("SET_PROFILE", res.data)
      }
      return state.profile
    },
  },
}

export default user
