import Api from "@/api"

function getDefaultState() {
  return {
    hasNew: false,
    notificationList: [],
    visible: false,
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
    SET_VISIBLE(state, visible) {
      state.visible = visible
    },
  },

  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async checkNew({ commit, state }) {
      let res = await Api.notification.hasNew()
      commit("SET_HAS_NEW", res.data)
      return state.hasNew
    },
    async getNotificationList({ commit, state }) {
      let res = await Api.notification.getNotificationList()
      commit("SET_NOTIFICATION_LIST", res.data)
      return state.notificationList
    },
    async dismissNotification({ state }, { slug }) {
      await Api.notification.dismissNotification(slug)
      return state.notificationList
    },
    async markAllAsRead({ commit, state }, { maxSlug }) {
      let res = await Api.notification.markAllAsRead(maxSlug)
      commit("SET_HAS_NEW", false) // no new notifications anymore
      commit("SET_NOTIFICATION_LIST", res.data)
      return state.notificationList
    },
    setVisible({ commit, state }, visible) {
      commit("SET_VISIBLE", visible)
      return state.visible
    },
  },
}

export default notification
