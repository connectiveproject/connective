import Api from "@/api"
import Utils from "@/helpers/utils"

function getDefaultState() {
  return {
    eventOrders: [],
    eventList: [],
    totalEvents: null,
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
    ADD_EVENTS_TO_LIST(state, eventList) {
      state.eventList.push(...eventList)
    },
    SET_EVENTS_LIST(state, eventList) {
      state.eventList = eventList
    },
    SET_EVENTS_TOTAL(state, total) {
      state.totalEvents = total
    },

  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getEventOrders(
      { commit, dispatch, rootGetters },
      { override = true, usePagination = true }
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
    async getEventList(
      { commit, state, rootGetters },
      { benchmarkDate, override = true, usePagination = true }
    ) {
      // :momentObject benchmarkDate: date to fetch the data near to (i.e., fetch the events in months around it)
      // :boolean override: whether to override the events list or not (i.e., extend)
      const mutation = override ? "SET_EVENTS_LIST" : "ADD_EVENTS_TO_LIST"
      const [startDate, endDate] = Utils.dateBenchmarkToRange(benchmarkDate, 30)
      const startDateString = Utils.dateToApiString(startDate)
      const endDateString = Utils.dateToApiString(endDate)
      let params = {
        start_time__gte: startDateString,
        start_time__lte: endDateString,
      }
      if (usePagination) {
        params = { ...params, ...rootGetters["pagination/apiParams"] }
      }
      let res = await Api.vendorEvent.getEventList(params)
      commit(mutation, res.data.results)
      commit("SET_EVENTS_TOTAL", res.data.count)
      return state.eventList
    },

  },
}

export default vendorEvent
