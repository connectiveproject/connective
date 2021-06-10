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
    UPDATE_JOIN_STATUS_IN_LIST(state, { programSlug, isConsumerJoined }) {
      const filteredProgram = state.programsList.filter(
        p => p.slug === programSlug
      )[0]
      filteredProgram.isConsumerJoined = isConsumerJoined
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
    async getProgram(ctx, programSlug) {
      // fetch and return a specific slug. does not save to store.
      let res = await Api.consumerProgram.getProgram(programSlug)
      return res.data
    },
    async getProgramMediaList(ctx, programSlug) {
      // fetch and return a specific program's media. does not save to store.
      let res = await Api.consumerProgram.getProgramMediaList(programSlug)
      return res.data.results
    },
    async getProgramsList({ commit, state, rootGetters }, override = true) {
      // :boolean override: whether to override the programs list or not (i.e., extend)
      const params = rootGetters["pagination/apiParams"]
      const mutation = override ? "SET_PROGRAM_LIST" : "ADD_PROGRAMS_TO_LIST"
      let res = await Api.consumerProgram.getProgramsList(params)
      commit(mutation, res.data.results)
      commit("SET_PROGRAMS_TOTAL", res.data.count)
      return state.programsList
    },
    async joinProgram({ commit }, programSlug) {
      const res = await Api.consumerProgram.joinProgram(programSlug)
      commit("UPDATE_JOIN_STATUS_IN_LIST", {
        programSlug,
        isConsumerJoined: true,
      })
      return res.data
    },
    async leaveProgram({ commit }, programSlug) {
      const res = await Api.consumerProgram.leaveProgram(programSlug)
      commit("UPDATE_JOIN_STATUS_IN_LIST", {
        programSlug,
        isConsumerJoined: false,
      })
      return res.data
    },
  },
}

export default program
