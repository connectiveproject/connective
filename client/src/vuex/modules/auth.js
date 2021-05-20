import Vue from "vue"
import Api from "../../api"
import { tokenCookieName } from "../../helpers/constants/constants"

function getDefaultState() {
  return {
    isAuthenticated: document.cookie.includes(`${tokenCookieName}=`),
  }
}

const auth = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    SET_AUTH(state, authState) {
      state.isAuthenticated = authState
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async login({ commit }, { email, password }) {
      let res = await Api.auth.login(email, password)
      Api.config.setToken(res.data.key)
      commit("SET_AUTH", true)
      Vue.$router.push({ name: "Dashboard" })
    },
    logout({ commit }, redirect = true) {
      Api.config.removeToken()
      commit("SET_AUTH", false)
      if (redirect) {
        Vue.$router.push({ path: "/" })
      }
    },
    resetPassword(ctx, { uid, token, pass, passConfirm, idNumber }) {
      return Api.auth.resetPassword(uid, token, pass, passConfirm, idNumber)
    },
  },
}

export default auth
