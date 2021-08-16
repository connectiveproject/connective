import Api from "../../api"

function getDefaultState() {
  return {
    groupList: [],
    totalGroups: null,
  }
}

const programGroup = {
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
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getGroup(ctx, groupSlug) {
      let res = await Api.programGroup.getGroup(groupSlug)
      return res.data
    },

    async getGroupList(
      { commit, state, rootGetters },
      { groupType, override, usePagination }
    ) {
      // :str groupType: which group type to fetch (if empty, fetch all groups)
      // :boolean override: whether to override the groups list or not (i.e., extend)
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      if (groupType) {
        params.group_type = groupType
      }
      const mutation = override ? "SET_GROUPS_LIST" : "ADD_GROUPS_TO_LIST"
      let res = await Api.programGroup.getGroupList(params)
      commit(mutation, res.data.results)
      commit("SET_GROUPS_TOTAL", res.data.count)
      return state.groupList
    },
    async getGroupsByFilter(ctx, params) {
      let res = await Api.programGroup.getGroupList(params)
      return res.data.results
    },
    async createGroup(ctx, data) {
      let res = await Api.programGroup.createGroup(data)
      return res.data
    },
    async updateGroup(ctx, { groupSlug, data }) {
      let res = await Api.programGroup.updateGroup(groupSlug, data)
      return res.data
    },
    deleteGroup(ctx, groupSlug) {
      return Api.programGroup.deleteGroup(groupSlug)
    },
    async getConsumers(ctx, groupSlug) {
      // get all consumers under a group
      // :str groupSlug: slug to fetch consumers by
      let res = await Api.programGroup.getConsumers(groupSlug)
      return res.data
    },
    async updateGroupConsumers(ctx, { groupSlug, consumerSlugs }) {
      // override group consumers and move the removed ones to container only
      // :Array consumerSlugs: consumers to apply to group
      let res = await Api.programGroup.updateGroupConsumers(
        groupSlug,
        consumerSlugs
      )
      return res.data
    },
  },
}

export default programGroup
