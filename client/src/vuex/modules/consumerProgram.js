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
    UPDATE_PROGRAM_IN_LIST(state, program) {
      const filteredProgram = state.programsList.filter(
        p => p.slug === program.slug
      )[0]
      Object.assign(filteredProgram, program)
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
    async joinProgram({ commit, dispatch }, programSlug) {
      const res = await Api.consumerProgram.joinProgram(programSlug)
      const program = await dispatch("getProgram", programSlug)
      commit("UPDATE_PROGRAM_IN_LIST", program)
      return res.data
    },
    async leaveProgram({ commit, dispatch }, programSlug) {
      const res = await Api.consumerProgram.leaveProgram(programSlug)
      const program = await dispatch("getProgram", programSlug)
      commit("UPDATE_PROGRAM_IN_LIST", program)
      return res.data
    },
  },
}

export default program
