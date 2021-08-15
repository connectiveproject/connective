import Api from "../../api"
import { SERVER } from "../../helpers/constants/constants"
function getDefaultState() {
  return {
    programsList: [],
    approvedOrdersList: [],
    totalPrograms: null,
    topConsumerRequestsStats: [],
  }
}

const program = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    ADD_PROGRAMS_TO_LIST(state, programsList) {
      state.programsList.push(...programsList)
    },
    UPDATE_PROGRAM_ORDER_IN_LIST(
      state,
      { programSlug, isOrdered, orderStatus }
    ) {
      const filteredProgram = state.programsList.filter(
        p => p.slug === programSlug
      )[0]
      filteredProgram.isOrdered = isOrdered
      filteredProgram.orderStatus = orderStatus
    },
    SET_PROGRAM_LIST(state, programsList) {
      state.programsList = programsList
    },
    SET_APPROVED_ORDERS_LIST(state, ordersList) {
      state.approvedOrdersList = ordersList
    },
    SET_PROGRAMS_TOTAL(state, total) {
      state.totalPrograms = total
    },
    SET_TOP_CONSUMER_REQUESTS_STATS(state, stats) {
      state.topConsumerRequestsStats = stats
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getProgram(ctx, slug) {
      // fetch and return a specific slug. does not save to store.
      let res = await Api.program.getProgram(slug)
      return res.data
    },
    async getProgramMediaList(ctx, slug) {
      // fetch and return a specific program's media. does not save to store.
      let res = await Api.program.getProgramMediaList(slug)
      return res.data.results
    },
    async getProgramsList(
      { commit, state, rootGetters },
      { override, usePagination }
    ) {
      // :boolean override: whether to override the programs list or not (i.e., extend)
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      const mutation = override ? "SET_PROGRAM_LIST" : "ADD_PROGRAMS_TO_LIST"
      let res = await Api.program.getProgramsList(params)
      commit(mutation, res.data.results)
      commit("SET_PROGRAMS_TOTAL", res.data.count)
      return state.programsList
    },
    async getApprovedOrdersList({ commit, state }) {
      let res = await Api.program.getOrdersList({
        status: SERVER.programOrderStatus.approved,
      })
      commit("SET_APPROVED_ORDERS_LIST", res.data.results)
      return state.approvedOrdersList
    },
    async createProgramOrder({ commit }, { schoolSlug, programSlug }) {
      // order program for a school
      const res = await Api.program.createProgramOrder(schoolSlug, programSlug)
      commit("UPDATE_PROGRAM_ORDER_IN_LIST", {
        programSlug,
        isOrdered: true,
        orderStatus: res.data.status,
      })
      return res.data
    },
    async reCreateProgramOrder({ commit }, { schoolSlug, programSlug }) {
      // order program after cancellation (order update instead of create)
      const res = await Api.program.reCreateProgramOrder(
        schoolSlug,
        programSlug
      )
      commit("UPDATE_PROGRAM_ORDER_IN_LIST", {
        programSlug,
        isOrdered: true,
        orderStatus: res.data.status,
      })
      return res.data
    },
    async cancelProgramOrder({ commit }, { schoolSlug, programSlug }) {
      // remove an order for a program in the school
      const res = await Api.program.cancelProgramOrder(schoolSlug, programSlug)
      commit("UPDATE_PROGRAM_ORDER_IN_LIST", {
        programSlug,
        isOrdered: false,
        orderStatus: res.data.status,
      })
      return res.data
    },
    async getTopConsumerRequestsStats({ commit, state }) {
      if (state.topConsumerRequestsStats.length) {
        return state.topConsumerRequestsStats
      }
      const res = await Api.program.getTopConsumerRequestsStats()
      commit("SET_TOP_CONSUMER_REQUESTS_STATS", res.data)
      return res.data
    },
  },
}

export default program
