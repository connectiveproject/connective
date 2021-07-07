import Vue from "vue"
import * as Sentry from "@sentry/vue"
import { Integrations } from "@sentry/tracing"
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
import "./filters"

Vue.config.productionTip = false
Vue.use(cookies)
Api.config.initAxiosSettings()

Sentry.init({
  Vue: Vue,
  dsn: "https://39d20f84436748028c8282bd7657ae61@o567262.ingest.sentry.io/5852636",
  integrations: [new Integrations.BrowserTracing()],
  // We recommend adjusting this value in production, or using tracesSampler
  // for finer control
  tracesSampleRate: 1.0,
})

new Vue({
  vuetify,
  router,
  store,
  i18n,
  render: h => h(App),
}).$mount("#app")
