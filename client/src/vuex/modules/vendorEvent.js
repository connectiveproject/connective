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
    UPDATE_EVENT_ORDER(state, order) {
      const filteredOrder = state.eventOrders.filter(
        o => o.slug === order.slug
      )[0]
      Object.assign(filteredOrder, order)
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
    async updateEventOrder({ commit }, { slug, data }) {
      const res = await Api.vendorEvent.updateEventOrder(slug, data)
      commit("UPDATE_EVENT_ORDER", res.data)
      return res.data
    },
  },
}

export default vendorEvent
