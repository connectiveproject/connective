import Vue from "vue"
import Api from "../../api"
import { TOKEN_COOKIE_NAME } from "../../helpers/constants/constants"

function getDefaultState() {
  return {
    isAuthenticated: document.cookie.includes(`${TOKEN_COOKIE_NAME}=`),
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
    async login({ commit }, { email, password, redirect = true }) {
      let res = await Api.auth.login(email, password)
      Api.config.setToken(res.data.key)
      commit("SET_AUTH", true)
      if (redirect) {
        Vue.$router.push({ name: "Dashboard" })
      }
    },
    async logout({ dispatch }, redirect = true) {
      Api.config.removeToken()
      await dispatch("flushState", null, { root: true })
      if (redirect) {
        Vue.$router.push({ path: "/" })
      }
    },
    async resetPassword(ctx, { uid, token, pass, passConfirm, idNumber }) {
      const res = await Api.auth.resetPassword(uid, token, pass, passConfirm, idNumber)
      return res.data
    },
    createPasswordRecoveryRequest(ctx, { email, recaptchaToken }) {
      return Api.auth.createPasswordRecoveryRequest(email, recaptchaToken)
    }
  },
}

export default auth
