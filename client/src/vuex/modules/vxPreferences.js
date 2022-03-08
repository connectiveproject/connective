import Api from "@/api"

function getDefaultState() {
  return {
    parameters: {},
  }
}

const vxEventList = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_PARAMETERS(state, parameters) {
      state.parameters = parameters
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getParameters({ commit, state }) {
      let res = await Api.apiParameters.getParameters()
      commit("SET_PARAMETERS", res.data.results[0])
      return state.parameters
    },
  },
}
export default vxEventList
