import Api from "../../api"
import Utils from "../../helpers/utils"

function getDefaultState() {
  return {
    eventList: [],
    totalEvents: null,
    eventOrders: [],
  }
}

const event = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
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
    SET_EVENT_ORDERS(state, orders) {
      state.eventOrders = orders
    },
    ADD_EVENT_ORDERS(state, orders) {
      state.eventOrders.push(...orders)
    },
    DELETE_EVENT_ORDER(state, slug) {
      state.eventOrders = state.eventOrders.filter(order => order.slug !== slug)
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getEventList(
      { commit, state, rootGetters },
      { benchmarkDate, override, usePagination }
    ) {
      // :momentObject benchmarkDate: date to fetch the data near to (i.e., fetch the events in months around it)
      // :boolean override: whether to override the events list or not (i.e., extend)
      const mutation = override ? "SET_EVENTS_LIST" : "ADD_EVENTS_TO_LIST"
      const [startDate, endDate] = Utils.dateBenchmarkToRange(benchmarkDate, 90)
      const startDateString = Utils.dateToApiString(startDate)
      const endDateString = Utils.dateToApiString(endDate)
      let params = {
        start_time__gte: startDateString,
        start_time__lte: endDateString,
      }
      if (usePagination) {
        params = [...params, ...rootGetters["pagination/apiParams"]]
      }
      let res = await Api.event.getEventList(params)
      commit(mutation, res.data.results)
      commit("SET_EVENTS_TOTAL", res.data.count)
      return state.eventList
    },
    async createEventOrder(ctx, data) {
      const res = await Api.event.createEventOrder(data)
      return res.data
    },
    async getEventOrders(
      { commit, dispatch, rootGetters },
      { override, usePagination }
    ) {
      const mutation = override ? "SET_EVENT_ORDERS" : "ADD_EVENT_ORDERS"
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      const res = await Api.event.getEventOrders(params)
      commit(mutation, res.data.results)
      dispatch("pagination/setTotalServerItems", res.data.count, { root: true })
      return res.data.results
    },
    async deleteEventOrder({ commit }, slug) {
      await Api.event.deleteEventOrder(slug)
      commit("DELETE_EVENT_ORDER", slug)
    },
  },
}

export default event
