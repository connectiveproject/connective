import Api from "../../api"

function getDefaultState() {
  return {
    eventList: [],
    totalEvents: null,
    feedPosts: [],
    totalFeedPosts: null,
  }
}

const eventFeedPost = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
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
    async getFeedPosts({ commit, rootGetters }, { override = true, usePagination = true } ) {
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      let res = await Api.eventFeedPost.getFeedPosts(params)
      const mutation = override
        ? "SET_FEED_POSTS_LIST"
        : "ADD_FEED_POSTS_TO_LIST"
      commit(mutation, res.data.results)
      commit("SET_FEED_POSTS_TOTAL", res.data.count)
      return res.data.results
    },
    async createFeedPost(ctx, data) {
      let res = await Api.eventFeedPost.createFeedPost(data)
      return res.data
    },
    async createPostImages(ctx, data) {
      let res = await Api.eventFeedPost.createPostImages(data)
      return res.data
    },
  },
}

export default eventFeedPost
