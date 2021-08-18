import Api from "../../api"

function getDefaultState() {
  return {}
}
const instructorProgramGroup = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getConsumers(ctx, groupSlug) {
      // get all consumers under a group
      // :str groupSlug: slug to fetch consumers by
      let res = await Api.instructorProgramGroup.getConsumers(groupSlug)
      return res.data.results
    },
  },
}

export default instructorProgramGroup
