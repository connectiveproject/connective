import Vue from "vue"
import Vuex from "vuex"
import cloneDeep from "lodash/cloneDeep"
import auth from "./modules/auth"
import user from "./modules/user"
import consumer from "./modules/consumer"
import coordinator from "./modules/coordinator"
import instructor from "./modules/instructor"
import vendor from "./modules/vendor"
import supervisor from "./modules/supervisor"
import school from "./modules/school"
import organization from "./modules/organization"
import program from "./modules/program"
import consumerProgram from "./modules/consumerProgram"
import vendorProgram from "./modules/vendorProgram"
import pagination from "./modules/pagination"
import loading from "./modules/loading"
import snackbar from "./modules/snackbar"
import introjs from "./modules/introjs"
import programGroup from "./modules/programGroup"
import vendorProgramGroup from "./modules/vendorProgramGroup"
import consumerProgramGroup from "./modules/consumerProgramGroup"
import instructorProgramGroup from "./modules/instructorProgramGroup"
import event from "./modules/event"
import consumerEvent from "./modules/consumerEvent"
import instructorEvent from "./modules/instructorEvent"
import vxEventList from "./modules/vxEventList"
import eventFeedPost from "./modules/eventFeedPost"
import vendorEvent from "./modules/vendorEvent"
import termsOfUse from "./modules/termsOfUse"
import notification from "./modules/notification"
import vxPreferences from "@/vuex/modules/vxPreferences"
import vxTags from "./modules/vxTags"

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    auth,
    user,
    consumer,
    coordinator,
    instructor,
    vendor,
    supervisor,
    school,
    organization,
    program,
    consumerProgram,
    vendorProgram,
    loading,
    snackbar,
    introjs,
    pagination,
    pagination2: cloneDeep(pagination),
    programGroup,
    vendorProgramGroup,
    consumerProgramGroup,
    instructorProgramGroup,
    event,
    consumerEvent,
    instructorEvent,
    vxEventList,
    eventFeedPost,
    vendorEvent,
    termsOfUse,
    notification,
    vxPreferences,
    vxTags,
  },
  actions: {
    flushState({ dispatch }) {
      // flush all modules
      const modules = Object.getOwnPropertyNames(this._modulesNamespaceMap)
      for (const m of modules) {
        if (!["loading/", "snackbar/", "introjs/"].includes(m)) {
          dispatch(`${m}flushState`)
        }
      }
    },
  },
})

export default store
