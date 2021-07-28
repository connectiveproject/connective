import Api from "../../api"

function getDefaultState() {
  return {
    eventOrders: [],
  }
}

const vendorEvent = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_EVENT_ORDERS(state, orders) {
      state.eventOrders = orders
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getEventOrders({ commit }) {
      const res = await Api.vendorEvent.getEventOrders()
      commit("SET_EVENT_ORDERS", res.data.results)
      return res.data.results
    },
  },
}

export default vendorEvent
