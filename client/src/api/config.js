import Vue from "vue"
import axios from "axios"
import Utils from "../helpers/utils"
import store from "../vuex/store"
import { TOKEN_COOKIE_NAME } from "../helpers/constants/constants"

function addTokenHeader(token) {
  axios.defaults.headers.common["Authorization"] = `Token ${token}`
}

function removeTokenHeader() {
  delete axios.defaults.headers.common["Authorization"]
}

function addInvalidTokenHandler() {
  axios.interceptors.response.use(
    // pop token if backend rejects it
    response => response,
    error => {
      if (error.response.data.detail === "Invalid token.") {
        config.removeToken()
        Vue.$router.push({
          name: "Error",
          params: { bodyKey: "errors.tokenExpired" },
        })
      }
      return Promise.reject(error)
    }
  )
}

function addProgressBarInterceptors() {
  axios.interceptors.request.use(config => {
    store.dispatch("loading/startLoading")
    return config
  })
  axios.interceptors.response.use(
    response => {
      store.dispatch("loading/doneLoading")
      return response
    },
    error => {
      store.dispatch("loading/doneLoading")
      return Promise.reject(error)
    }
  )
}

function addPayloadCaseConversion() {
  // add camelCase <-> snake_case conversion on request and response
  axios.defaults.transformResponse = [
    (data, headers) => {
      if (data && headers["content-type"].includes("application/json")) {
        let converted = Utils.convertKeysCase(JSON.parse(data), "camel")
        return JSON.stringify(converted)
      }
    },
    ...axios.defaults.transformResponse,
  ]
  axios.defaults.transformRequest = [
    data => {
      if (data) {
        return Utils.convertKeysCase(data, "snake")
      }
    },
    ...axios.defaults.transformRequest,
  ]
}

const config = {
  initAxiosSettings() {
    // init app's axios settings - set token header is token exists, handle token backend expiry
    let token = Vue.$cookies.get(TOKEN_COOKIE_NAME)
    if (token) {
      addTokenHeader(token)
    }
    addInvalidTokenHandler()
    addProgressBarInterceptors()
    addPayloadCaseConversion()
  },

  setToken(token) {
    // save token as cookie and as axios header
    // :string token: the token to use
    Vue.$cookies.set(TOKEN_COOKIE_NAME, token)
    addTokenHeader(token)
  },

  removeToken() {
    // remove token from cookie and axios header
    Vue.$cookies.erase(TOKEN_COOKIE_NAME)
    removeTokenHeader()
  },
}

export default config
