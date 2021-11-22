import Api from "../../api"
import Utils from "../../helpers/utils"

function getDefaultState() {
  return {
    eventList: [],
    totalEvents: null,
  }
}

const consumerEvent = {
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
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },

    async getEvent(ctx, slug) {
      let res = await Api.consumerEvent.getEvent(slug)
      return res.data
    },

    async getEventList(
      { commit, state, rootGetters },
      { benchmarkDate, override = true, usePagination = true }
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
        params = { ...params, ...rootGetters["pagination/apiParams"] }
      }
      let res = await Api.consumerEvent.getEventList(params)
      commit(mutation, res.data.results)
      commit("SET_EVENTS_TOTAL", res.data.count)
      return state.eventList
    },

    async getPastEvents({ rootGetters }, { daysAgo, usePagination = true, ignoreCanceled = false }) {
      // :Number daysAgo: days ago to get the events from (e.g., 21 means all events 3 weeks ago until today)
      const startDateString = Utils.dateToApiString(
        Utils.addDaysToToday(-daysAgo)
      )
      const endDateString = Utils.dateToApiString(Utils.addDaysToToday(0))
      let params = {
        start_time__gte: startDateString,
        start_time__lte: endDateString,
      }
      if (usePagination) {
        params = { ...params, ...rootGetters["pagination/apiParams"] }
      }
      if (ignoreCanceled) {
        params.is_canceled = false
      }
      let res = await Api.consumerEvent.getEventList(params)
      return res.data.results
    },

    async createEventFeedback(ctx, data) {
      let res = await Api.consumerEvent.createEventFeedback(data)
      return res.data
    },
  },
}

export default consumerEvent
