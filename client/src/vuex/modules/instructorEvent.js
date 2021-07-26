import Api from "../../api"
import Utils from "../../helpers/utils"

function getDefaultState() {
  return {
    eventList: [],
    totalEvents: null,
    feedPosts: [],
    totalFeedPosts: null,
  }
}

const instructorEvent = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_EVENTS_LIST(state, eventList) {
      state.eventList = eventList
    },
    SET_EVENTS_TOTAL(state, total) {
      state.totalEvents = total
    },
    SET_FEED_POSTS_LIST(state, posts) {
      state.feedPosts = posts
    },
    SET_FEED_POSTS_TOTAL(state, total) {
      state.totalFeedPosts = total
    },
    ADD_FEED_POSTS_TO_LIST(state, posts) {
      state.feedPosts.push(...posts)
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getEvent(ctx, slug) {
      let res = await Api.instructorEvent.getEvent(slug)
      return res.data
    },
    async updateEvent(ctx, { slug, data }) {
      let res = await Api.instructorEvent.updateEvent(slug, data)
      return res.data
    },
    async getFeedPosts({ commit, rootGetters }, override = true) {
      const params = rootGetters["pagination/apiParams"]
      let res = await Api.instructorEvent.getFeedPosts(params)
      const mutation = override
        ? "SET_FEED_POSTS_LIST"
        : "ADD_FEED_POSTS_TO_LIST"
      commit(mutation, res.data.results)
      commit("SET_FEED_POSTS_TOTAL", res.data.count)
      return res.data.results
    },
    async createFeedPost(ctx, data) {
      let res = await Api.instructorEvent.createFeedPost(data)
      return res.data
    },
    async createPostImages(ctx, data) {
      let res = await Api.instructorEvent.createPostImages(data)
      return res.data
    },
    async getPastEvents({ commit, state }, { daysAgo, unsummarizedOnly }) {
      // :Number daysAgo: days ago to get the events from (e.g., 21 means all events 3 weeks ago until today)
      const startDateString = Utils.dateToApiString(
        Utils.addDaysToToday(-daysAgo)
      )
      const endDateString = Utils.dateToApiString(Utils.addDaysToToday(0))
      const params = {
        start_time__gte: startDateString,
        start_time__lte: endDateString,
      }
      if (unsummarizedOnly) {
        params.has_summary = false
      }
      let res = await Api.instructorEvent.getEventList(params)
      commit("SET_EVENTS_LIST", res.data.results)
      commit("SET_EVENTS_TOTAL", res.data.count)
      return state.eventList
    },
  },
}

export default instructorEvent
