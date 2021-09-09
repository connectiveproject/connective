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
  },
  getters: {
    isConsumer(state) {
      return state.userDetails.userType === SERVER.userTypes.consumer
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
      return state.userDetails
    },
    async updateUserDetails({ commit, state }, { slug, userDetails }) {
      let res = await Api.user.updateUserDetails(slug, userDetails)
      commit("SET_USER_DETAILS", res.data)
      return state.userDetails
    },
  },
}

export default user
