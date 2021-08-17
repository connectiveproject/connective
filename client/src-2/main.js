import Vue from "vue"
import App from "../src/App.vue"
import router from "./router"
import store from "../src/vuex/store"
import vuetify from "../src/plugins/vuetify"
import i18n from "../src/plugins/i18n"
import cookies from "../src/plugins/cookies"
import Api from "../src/api"
import "../src/helpers/validators"
import "intro.js/introjs.css"
import "intro.js/introjs-rtl.css"
import "nprogress/nprogress.css"
import "../src/styles/main.scss"
import "../src/filters"

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
