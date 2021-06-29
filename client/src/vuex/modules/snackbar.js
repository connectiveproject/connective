const snackbar = {
  namespaced: true,
  state: {
    text: "",
  },
  mutations: {
    SHOW_MESSAGE(state, text) {
      state.text = text
    },
  },
  actions: {
    showMessage({ commit }, text) {
      commit("SHOW_MESSAGE", text)
    },
  },
}

export default snackbar
