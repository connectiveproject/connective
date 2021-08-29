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
    async getConsumers(
      { dispatch, rootGetters },
      { groupSlugs, usePagination }
    ) {
      // get all consumers under a group
      // :array groupSlug: array of group slugs to fetch consumers by
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      let res = await Api.programGroup.getConsumers(groupSlugs, params)
      if (usePagination) {
        dispatch("pagination/setTotalServerItems", res.data.count, {
          root: true,
        })
      }
      return res.data.results
    },
  },
}

export default instructorProgramGroup
