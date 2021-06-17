import Api from "../../api"
import Utils from "../../helpers/utils"

function getDefaultState() {
  return {
    eventList: [],
    totalEvents: null,
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
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getEventList({ commit, state }, { benchmarkDate, override }) {
      // :momentObject benchmarkDate: date to fetch the data near to (i.e., fetch the events in months around it)
      // :boolean override: whether to override the events list or not (i.e., extend)
      const mutation = override ? "SET_EVENTS_LIST" : "ADD_EVENTS_TO_LIST"
      const [startDate, endDate] = Utils.dateBenchmarkToRange(benchmarkDate, 60)
      const startDateString = Utils.dateToApiString(startDate)
      const endDateString = Utils.dateToApiString(endDate)
      const params = {
        start_time__gte: startDateString,
        start_time__lte: endDateString,
      }
      let res = await Api.event.getEventList(params)
      commit(mutation, res.data.results)
      commit("SET_EVENTS_TOTAL", res.data.count)
      return state.eventList
    },
  },
}

export default event
