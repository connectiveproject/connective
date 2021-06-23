import Api from "../../api"

function getDefaultState() {
  return {
    profile: {
      gender: null,
      profilePicture: null,
    },
  }
}

const instructor = {
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
      if (!state.profile.gender) {
        // fetch if not in cache
        let res = await Api.instructor.getProfile()
        commit("SET_PROFILE", res.data)
      }
      return state.profile
    },
    async updateProfile({ commit, state }, { slug, profile }) {
      let res = await Api.instructor.updateProfile(slug, profile)
      commit("SET_PROFILE", res.data)
      return state.profile
    },
  },
}

export default instructor
