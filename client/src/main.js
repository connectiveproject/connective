import Vue from "vue"
import App from "./App.vue"
import router from "./router"
import store from "./vuex/store"
import vuetify from "./plugins/vuetify"
import i18n from "./plugins/i18n"
import cookies from "./plugins/cookies"
import Api from "./api"
import "./helpers/validators"
import "nprogress/nprogress.css"
import "./styles/main.scss"

Vue.config.productionTip = false
Vue.use(cookies)
Api.config.initAxiosSettings()

const vm = new Vue({
  vuetify,
  router,
  store,
  i18n,
  render: h => h(App),
}).$mount("#app")

export default vm
