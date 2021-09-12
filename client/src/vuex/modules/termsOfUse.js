import Api from "@/api"

function getDefaultState() {
  return {}
}

const user = {
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
    async getTermsOfUseTexts() {
      const res = await Api.termsOfUse.getTermsOfUseTexts()
      return res.data.results
    },
    updateTermsOfUseAcceptance() {
      return Api.termsOfUse.updateTermsOfUseAcceptance()
    },
  },
}

export default user
