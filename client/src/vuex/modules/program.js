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
      let res = await Api.program.getProgramMediaListApiUrl(slug)
      return res.data
    },
    async getProgramsList({ commit, state, rootGetters }, override = true) {
      // :boolean override: whether to override the programs list or not (i.e., extend)
      const params = rootGetters["pagination/apiParams"]
      const mutation = override ? "SET_PROGRAM_LIST" : "ADD_PROGRAMS_TO_LIST"
      let res = await Api.program.getProgramsList(params)
      commit(mutation, res.data)
      commit("SET_PROGRAMS_TOTAL", parseInt(res.headers["x-total-count"]))
      return state.programsList
    },
  },
}

export default program
