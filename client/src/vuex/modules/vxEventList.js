import Api from "@/api"
import Utils from "@/helpers/utils"

function getDefaultState() {
  return {
    pastEvents: [],
  }
}

const vxEventList = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    ADD_PAST_EVENTS(state, eventList) {
      state.pastEvents.push(...eventList)
    },
    SET_PAST_EVENTS(state, eventList) {
      state.pastEvents = eventList
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getPastEvents(
      { commit, state, rootGetters },
      { override = true, usePagination = true }
    ) {
      const mutation = override ? "SET_PAST_EVENTS" : "ADD_PAST_EVENTS"
      let params = {
        start_time__lte: Utils.dateToApiString(Utils.addDaysToToday(0)),
      }
      if (usePagination) {
        params = { ...params, ...rootGetters["pagination/apiParams"] }
      }
      let res = await Api.apiEventList.getEventList(params)
      commit(mutation, res.data.results)
      return state.pastEvents
    },
    getPastEventsExportFile({ rootGetters }, { usePagination = true }) {
      let params = {
        start_time__lte: Utils.dateToApiString(Utils.addDaysToToday(0)),
      }
      if (usePagination) {
        params = { ...params, ...rootGetters["pagination/apiParams"] }
      }
      Api.apiEventList.getPastEventsExportFile(params).then(res => {
        Utils.downloadTextAsFile("events.csv", res.request.response)
        return res
      })
    },
  },
}
export default vxEventList
