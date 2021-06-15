import Api from "../../api"

function getDefaultState() {
  return {
    groupList: [],
    totalGroups: null,
  }
}

const programsGroups = {
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
    SET_GROUPS_TOTAL(state, total) {
      state.totalGroups = total
    },
  },
  actions: {
    async getGroupList({ commit, state, rootGetters }, override = true) {
      // :boolean override: whether to override the groups list or not (i.e., extend)
      const params = rootGetters["pagination/apiParams"]
      const mutation = override ? "SET_GROUPS_LIST" : "ADD_GROUPS_TO_LIST"
      let res = await Api.programGroups.getGroupList(params)
      commit(mutation, res.data.results)
      commit("SET_GROUPS_TOTAL", res.data.count)
      return state.groupList
    },
  },
}

export default programsGroups
