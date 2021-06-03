import Api from "../../api"

function getDefaultState() {
  return {
    programsList: [],
    totalPrograms: null,
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
    SET_PROGRAMS_TOTAL(state, total) {
      state.totalPrograms = total
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
    async getProgramsList({ commit, state, rootGetters }, override = true) {
      // :boolean override: whether to override the programs list or not (i.e., extend)
      const params = rootGetters["pagination/apiParams"]
      const mutation = override ? "SET_PROGRAM_LIST" : "ADD_PROGRAMS_TO_LIST"
      let res = await Api.program.getProgramsList(params)
      commit(mutation, res.data.results)
      commit("SET_PROGRAMS_TOTAL", res.data.count)
      return state.programsList
    },
    async orderProgram({ commit }, { schoolSlug, programSlug }) {
      // order program for a school
      const res = await Api.program.orderProgram(schoolSlug, programSlug)
      commit("UPDATE_PROGRAM_ORDER_IN_LIST", {
        programSlug,
        isOrdered: true,
        orderStatus: res.data.status,
      })
      return res.data
    },
    async reOrderProgram({ commit }, { schoolSlug, programSlug }) {
      // order program after cancellation (order update instead of create)
      const res = await Api.program.reOrderProgram(schoolSlug, programSlug)
      commit("UPDATE_PROGRAM_ORDER_IN_LIST", {
        programSlug,
        isOrdered: true,
        orderStatus: res.data.status,
      })
      return res.data
    },
    async disOrderProgram({ commit }, { schoolSlug, programSlug }) {
      // remove an order for a program in the school
      const res = await Api.program.disOrderProgram(schoolSlug, programSlug)
      commit("UPDATE_PROGRAM_ORDER_IN_LIST", {
        programSlug,
        isOrdered: false,
        orderStatus: res.data.status,
      })
      return res.data
    },
  },
}

export default program
