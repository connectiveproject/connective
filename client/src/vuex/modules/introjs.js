import i18n from "../../plugins/i18n"

const introjs = {
  namespaced: true,
  state: {
    subscriptions: 0,
  },
  mutations: {
    INCREMENT_SUBSCRIPTION(state) {
      state.subscriptions += 1
    },
    DECREMENT_SUBSCRIPTION(state) {
      state.subscriptions -= 1
    },
  },
  actions: {
    triggerIntro({ state, dispatch }) {
      // this action subscribed by components
      if (!state.subscriptions) {
        dispatch(
          "snackbar/showMessage",
          i18n.t("errors.explanationForThisPageDoesNotExist"),
          { root: true }
        )
      }
    },
    incrementSubscription({ commit }) {
      commit("INCREMENT_SUBSCRIPTION")
    },
    decrementSubscription({ commit }) {
      commit("DECREMENT_SUBSCRIPTION")
    },
  },
}

export default introjs
