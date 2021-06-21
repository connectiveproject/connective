import Vue from "vue"
import VueRouter from "vue-router"
import i18n from "../plugins/i18n"
import {
  checkRegistrationStatus,
  loginOrFlushStore,
  initPrograms,
  initConsumerPrograms,
  flushPagination,
  flushToken,
  PopulateConsumerData,
  PopulateCoordinatorData,
  fetchProgramDetails,
} from "./guards"
import Welcome from "../layouts/Welcome.vue"
import ManagementDashboard from "../layouts/ManagementDashboard.vue"
import StudentDashboard from "../layouts/StudentDashboard.vue"
import MyActivity from "../layouts/MyActivity/MyActivity.vue"
import ConsumerMyActivity from "../layouts/MyActivity/ConsumerMyActivity.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import Profile from "../views/Profile.vue"
import ConsumerProfile from "../views/ConsumerProfile.vue"
import SchoolDetails from "../views/SchoolDetails.vue"
import ProgramsExplorer from "../views/ProgramsExplorer/ProgramsExplorer.vue"
import ConsumerProgramsExplorer from "../views/ProgramsExplorer/ConsumerProgramsExplorer.vue"
import Invite from "../views/Invite/Invite.vue"
import ResetPassword from "../views/ResetPassword.vue"
import GenericError from "../views/Error.vue"
import ProgramModal from "../views/ProgramModal"
import MyGroups from "../views/MyGroups/MyGroups"
import ConsumerMyGroups from "../views/MyGroups/ConsumerMyGroups"
import MyEvents from "../views/MyEvents/MyEvents"
import ConsumerMyEvents from "../views/MyEvents/ConsumerMyEvents"

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    redirect: `/${i18n.locale}/welcome/login`,
  },
  {
    path: "/:lang",
    component: {
      render(c) {
        return c("router-view")
      },
    },
    children: [
      {
        path: "welcome",
        name: "Welcome",
        component: Welcome,
        children: [
          {
            path: "register",
            name: "Register",
            component: Register,
          },
          {
            path: "reset-password/:uid/:token",
            name: "ResetPassword",
            component: ResetPassword,
            beforeEnter: flushToken,
            props: true,
          },
          {
            path: "login",
            name: "Login",
            component: Login,
            beforeEnter: loginOrFlushStore,
          },
        ],
      },
      {
        path: "dashboard",
        name: "Dashboard",
        component: {
          render(c) {
            return c("router-view")
          },
        },
        beforeEnter: checkRegistrationStatus,
      },
      {
        path: "student-dashboard",
        component: StudentDashboard,
        beforeEnter: PopulateConsumerData,
        children: [
          {
            path: "",
            name: "StudentDashboard",
            redirect: { name: "ConsumerProfile" },
          },
          {
            path: "profile",
            name: "ConsumerProfile",
            component: ConsumerProfile,
          },
          {
            path: "programs-explorer",
            name: "ConsumerProgramsExplorer",
            component: ConsumerProgramsExplorer,
            beforeEnter: initConsumerPrograms,
            children: [
              {
                path: "program-modal/:slug",
                name: "ConsumerProgramModal",
                component: ProgramModal,
                beforeEnter: fetchProgramDetails,
                props: true,
              },
            ],
          },
          {
            path: "my-activity",
            component: ConsumerMyActivity,
            children: [
              {
                path: "",
                name: "ConsumerMyActivity",
                redirect: { name: "ConsumerMyGroups" },
              },
              {
                path: "my-groups",
                name: "ConsumerMyGroups",
                component: ConsumerMyGroups,
              },
              {
                path: "my-events",
                name: "ConsumerMyEvents",
                component: ConsumerMyEvents,
              },
            ],
          },
        ],
      },
      {
        path: "management-dashboard",
        component: ManagementDashboard,
        beforeEnter: PopulateCoordinatorData,
        children: [
          {
            path: "",
            name: "ManagementDashboard",
            redirect: { name: "Profile" },
          },
          {
            path: "profile",
            name: "Profile",
            component: Profile,
          },
          {
            path: "schoolDetails",
            name: "SchoolDetails",
            component: SchoolDetails,
          },
          {
            path: "invite",
            name: "Invite",
            component: Invite,
            beforeEnter: flushPagination,
          },
          {
            path: "programs-explorer",
            name: "ProgramsExplorer",
            component: ProgramsExplorer,
            beforeEnter: initPrograms,
            children: [
              {
                path: "program-modal/:slug",
                name: "ProgramModal",
                component: ProgramModal,
                beforeEnter: fetchProgramDetails,
                props: true,
              },
            ],
          },
          {
            path: "my-activity",
            component: MyActivity,
            children: [
              {
                path: "",
                name: "MyActivity",
                redirect: { name: "MyGroups" },
              },
              {
                path: "my-groups",
                name: "MyGroups",
                component: MyGroups,
              },
              {
                path: "my-events",
                name: "MyEvents",
                component: MyEvents,
              },
            ],
          },
        ],
      },
      {
        path: "error",
        name: "Error",
        component: GenericError,
        props: true,
      },
    ],
  },
]

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

// make accessible across modules, to avoid Vue.use(VueRouter) reuse
Vue.$router = router
export default router
