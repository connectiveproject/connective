import Api from "../../api"

function getDefaultState() {
  return {
    groupList: [],
  }
}

const vendorProgramGroup = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    ADD_GROUPS_TO_LIST(state, groupList) {
      state.groupList.push(...groupList)
    },
    SET_GROUPS_LIST(state, groupList) {
      state.groupList = groupList
    },
    UPDATE_GROUP_IN_LIST(state, group) {
      const filteredGroup = state.groupList.filter(
        g => g.slug === group.slug
      )[0]
      Object.assign(filteredGroup, group)
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getGroupList(
      { commit, state, dispatch, rootGetters },
      { groupType, override = true, usePagination = true }
    ) {
      // :str groupType: which group type to fetch (if empty, fetch all groups)
      // :boolean override: whether to override the groups list or not (i.e., extend)
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      if (groupType) {
        params.group_type = groupType
      }
      const mutation = override ? "SET_GROUPS_LIST" : "ADD_GROUPS_TO_LIST"
      let res = await Api.vendorProgramGroup.getGroupList(params)
      commit(mutation, res.data.results)
      dispatch("pagination/setTotalServerItems", res.data.count, { root: true })
      return state.groupList
    },
    async updateGroup({ commit }, { groupSlug, data }) {
      let res = await Api.vendorProgramGroup.updateGroup(groupSlug, data)
      commit("UPDATE_GROUP_IN_LIST", res.data)
      return res.data
    },
  },
}

export default vendorProgramGroup
