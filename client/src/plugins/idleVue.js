import Vue from "vue"
import IdleVue from "idle-vue"
import store from "@/vuex/store"
import { SESSION_IDLE_TIMEOUT_MINUTES } from "@/helpers/constants/constants"

Vue.use(IdleVue, {
  eventEmitter: new Vue(),
  idleTime: SESSION_IDLE_TIMEOUT_MINUTES * 60 * 1000,
  startAtIdle: false,
})

export function onIdle() {
  if (store.state.auth.isAuthenticated) {
    store.dispatch("auth/logout", false)
    Vue.$router.push({
      name: "Error",
      params: {
        titleKey: "errors.sessionExpired",
        bodyKey: "errors.sessionExpiredPleaseLoginAgain",
      },
    })
  }
}
