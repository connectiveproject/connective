import Api from "../../api"

function getDefaultState() {
  return {
    profile: {
      gender: null,
      profilePicture: null,
    },
  }
}

const consumer = {
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
        let res = await Api.consumer.getProfile()
        commit("SET_PROFILE", res.data)
      }
      return state.profile
    },
    async updateProfile({ commit, state }, { slug, profile }) {
      let res = await Api.consumer.updateProfile(slug, profile)
      commit("SET_PROFILE", res.data)
      return state.profile
    },
  },
}

// i.e., student
export default consumer
