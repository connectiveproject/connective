import Api from "@/api"

function getDefaultState() {
  return {}
}

const termsOfUse = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getTermsOfUseText() {
      const res = await Api.termsOfUse.getTermsOfUseText()
      return res.data.results
    },
    updateTermsOfUseAcceptance() {
      return Api.termsOfUse.updateTermsOfUseAcceptance()
    },
  },
}

export default termsOfUse
