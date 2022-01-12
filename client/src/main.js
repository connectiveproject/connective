import "./analytics"
import Vue from "vue"
import App from "@/App.vue"
import router from "@/router"
import store from "@/vuex/store"
import vuetify from "@/plugins/vuetify"
import i18n from "@/plugins/i18n"
import cookies from "@/plugins/cookies"
import Api from "@/api"
import "@/filters"
import "@/helpers/validators"
import "intro.js/introjs.css"
import "nprogress/nprogress.css"
import Utils from "@/helpers/utils"

Vue.use(cookies)
Vue.config.productionTip = false

Api.config.initAxiosSettings()

new Vue({
  vuetify,
  router,
  store,
  i18n,
  render: h => h(App),
}).$mount("#app")

if (Utils.checkRtl()) {
  import("intro.js/introjs-rtl.css")
}

// eslint-disable-next-line no-unused-vars
router.afterEach((to, from) => {
  store.dispatch("notification/checkNew")
})
