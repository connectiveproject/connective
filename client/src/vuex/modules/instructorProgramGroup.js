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
    async getConsumers(ctx, groupSlugs) {
      // get all consumers under a group
      // :array groupSlugs: array of group slugs to fetch consumers by
      let res = await Api.instructorProgramGroup.getConsumers(groupSlugs)
      return res.data.results
    },
  },
}

export default instructorProgramGroup
