import NProgress from "nprogress"

NProgress.configure({ showSpinner: false })

const loading = {
  namespaced: true,
  state: {
    waitingApiCalls: 0,
  },
  mutations: {
    INCREMENT_API_CALLS(state) {
      state.waitingApiCalls += 1
    },
    DECREMENT_API_CALLS(state) {
      state.waitingApiCalls -= 1
    },
  },
  actions: {
    startLoading({ commit, state }) {
      if (state.waitingApiCalls === 0) {
        NProgress.start()
      }
      commit("INCREMENT_API_CALLS")
    },
    doneLoading({ commit, state }) {
      commit("DECREMENT_API_CALLS")
      if (state.waitingApiCalls === 0) {
        NProgress.done()
      }
    },
  },
}

export default loading
