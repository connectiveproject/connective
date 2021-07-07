import Api from "../../api"

function getDefaultState() {
  return {
    programList: [],
  }
}

const vendorProgram = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_PROGRAM_LIST(state, programList) {
      state.programList = programList
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getProgram(ctx, programSlug) {
      // fetch and return a specific slug. does not save to store.
      let res = await Api.vendorProgram.getProgram(programSlug)
      return res.data
    },
    async getProgramMediaList(ctx, programSlug) {
      // fetch and return a specific program's media. does not save to store.
      let res = await Api.vendorProgram.getProgramMediaList(programSlug)
      return res.data.results
    },
    deleteProgramMedia(ctx, mediaSlug) {
      return Api.vendorProgram.deleteProgramMedia(mediaSlug)
    },
    async createProgramMedia(ctx, payload) {
      // :Object payload: should contain activity & videoUrl/imageUrl
      let res = await Api.vendorProgram.createProgramMedia(payload)
      return res.data
    },
    async getProgramList({ commit }) {
      let res = await Api.vendorProgram.getProgramList()
      commit("SET_PROGRAM_LIST", res.data.results)
      return res.data.results
    },
    async createProgram(ctx, payload) {
      let res = await Api.vendorProgram.createProgram(payload)
      return res.data
    },
    async updateProgram(ctx, { programSlug, payload }) {
      let res = await Api.vendorProgram.updateProgram(programSlug, payload)
      return res.data
    },
    deleteProgram(ctx, programSlug) {
      return Api.vendorProgram.deleteProgram(programSlug)
    },
  },
}

export default vendorProgram
