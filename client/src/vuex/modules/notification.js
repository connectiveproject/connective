import Api from "@/api"

function getDefaultState() {
  return {
    hasNew: false,
    notificationList: []
  }
}

const notification = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_NOTIFICATION_LIST(state, notificationList) {
      state.notificationList = notificationList
    },
    SET_HAS_NEW(state, hasNew) {
      state.hasNew = hasNew
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async hasNew({ commit, state }) {
      let res = await Api.notification.hasNew()
      commit("SET_HAS_NEW", res.data)
      return state.hasNew
    },
    async getNotificationList({ commit, state }) {
      let res = await Api.notification.getNotificationList() // TODO implement
      commit("SET_NOTIFICATION_LIST", res.data)
      return state.notificationList
    },
  },
}

export default notification
