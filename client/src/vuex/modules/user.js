import Api from "../../api"

function getDefaultState() {
  return {
    userDetails: {
      slug: null,
      first_name: null,
      last_name: null,
      email: null,
      url: null,
      groups: [],
    },
    profile: {
      user: null,
      phoneNumber: null,
      profilePicture: null,
      jobDescription: null,
    },
    connectiveProfile: {
      // connective-specific profile attributes
      user: null,
      school: null,
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
    SET_PROFILE(state, userProfile) {
      state.profile = userProfile
    },
    SET_CONNECTIVE_PROFILE(state, connectiveProfile) {
      state.connectiveProfile = connectiveProfile
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
    async getProfile({ commit, state }) {
      if (!state.profile.phoneNumber) {
        // fetch if not in cache
        let res = await Api.user.getProfile()
        commit("SET_PROFILE", res.data)
      }
      return state.profile
    },
    async updateProfile({ commit, state }, { slug, profile }) {
      let res = await Api.user.updateProfile(slug, profile)
      commit("SET_PROFILE", res.data)
      return state.profile
    },
    async getConnectiveProfile({ commit, state }) {
      if (!state.connectiveProfile.user) {
        // fetch if not in cache
        let res = await Api.user.getConnectiveProfile()
        commit("SET_CONNECTIVE_PROFILE", res.data[0])
      }
      return state.connectiveProfile
    },
  },
}

export default user
