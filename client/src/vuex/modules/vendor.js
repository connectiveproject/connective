import Api from "../../api"

function getDefaultState() {
  return {
    profile: {
      phoneNumber: null,
      profilePicture: null,
    },
  }
}

const vendor = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_PROFILE(state, userProfile) {
      state.profile = userProfile
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getProfile({ commit, state }) {
      if (!state.profile.phoneNumber) {
        // fetch if not in cache
        let res = await Api.vendor.getProfile()
        commit("SET_PROFILE", res.data)
      }
      return state.profile
    },
    async updateProfile({ commit, state }, { slug, profile }) {
      let res = await Api.vendor.updateProfile(slug, profile)
      commit("SET_PROFILE", res.data)
      return state.profile
    },
  },
}

// i.e., org manager
export default vendor
