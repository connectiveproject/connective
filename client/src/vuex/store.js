import Vue from "vue"
import Vuex from "vuex"
import auth from "./modules/auth"
import user from "./modules/user"
import consumer from "./modules/consumer"
import coordinator from "./modules/coordinator"
import instructor from "./modules/instructor"
import supervisor from "./modules/supervisor"
import vendor from "./modules/vendor"
import school from "./modules/school"
import organization from "./modules/organization"
import program from "./modules/program"
import consumerProgram from "./modules/consumerProgram"
import vendorProgram from "./modules/vendorProgram"
import pagination from "./modules/pagination"
import loading from "./modules/loading"
import snackbar from "./modules/snackbar"
import programGroup from "./modules/programGroup"
import consumerProgramGroup from "./modules/consumerProgramGroup"
import instructorProgramGroup from "./modules/instructorProgramGroup"
import event from "./modules/event"
import consumerEvent from "./modules/consumerEvent"
import instructorEvent from "./modules/instructorEvent"

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    auth,
    user,
    consumer,
    coordinator,
    supervisor,
    instructor,
    vendor,
    school,
    organization,
    program,
    consumerProgram,
    vendorProgram,
    loading,
    snackbar,
    pagination,
    programGroup,
    consumerProgramGroup,
    instructorProgramGroup,
    event,
    consumerEvent,
    instructorEvent,
  },
  actions: {
    flushState({ dispatch }) {
      // flush all modules
      const modules = Object.getOwnPropertyNames(this._modulesNamespaceMap)
      for (const m of modules) {
        if (!["loading/", "snackbar/"].includes(m)) {
          dispatch(`${m}flushState`)
        }
      }
    },
  },
})

export default store
