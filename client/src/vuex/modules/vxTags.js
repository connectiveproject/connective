import Api from "@/api"

function getDefaultState() {
  return {
    tags: []
  }
}
const vxTags = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_ALL_TAGS(state, tags) {
      state.tags = tags
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    // TODO - tags are not changing very often, we need to cache it to avoid the API call again and again.
    // Is this the correct way to do it?
    async loadTags({ state, commit }) {
      if (state.tags && state.tags.length > 0) {
        return state.tags
      }
      const res = await Api.apiTags.getAllTags()
      commit("SET_ALL_TAGS", res.data.results)
      return res.data.results
    },
  },
}

export default vxTags
