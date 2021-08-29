import Api from "@/api"

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
    async getEventOrders(
      { commit, dispatch, rootGetters },
      { override, usePagination }
    ) {
      const mutation = override ? "SET_EVENT_ORDERS" : "ADD_EVENT_ORDERS"
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      const res = await Api.vendorEvent.getEventOrders(params)
      commit(mutation, res.data.results)
      dispatch("pagination/setTotalServerItems", res.data.count, { root: true })
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
