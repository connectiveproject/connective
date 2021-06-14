import Vue from "vue"
import Vuex from "vuex"
import auth from "./modules/auth"
import user from "./modules/user"
import consumer from "./modules/consumer"
import coordinator from "./modules/coordinator"
import school from "./modules/school"
import program from "./modules/program"
import consumerProgram from "./modules/consumerProgram"
import pagination from "./modules/pagination"
import loading from "./modules/loading"

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    auth,
    user,
    consumer,
    coordinator,
    school,
    program,
    consumerProgram,
    loading,
    pagination,
  },
  actions: {
    flushState({ dispatch }) {
      // flush all modules
      const modules = Object.getOwnPropertyNames(this._modulesNamespaceMap)
      for (const m of modules) {
        if (m !== "loading/") {
          dispatch(`${m}flushState`)
        }
      }
    },
  },
})

export default store
