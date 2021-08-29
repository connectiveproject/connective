import Vue from "vue"
import VueRouter from "vue-router"
import routes from "@/router/routes"
import guards from "@/router/guards"

Vue.use(VueRouter)

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

router.beforeEach(guards.flushPagination)


// make accessible across modules, to avoid Vue.use(VueRouter) reuse
Vue.$router = router
export default router
