import Vue from "vue"
import VueRouter from "vue-router"
import i18n from "../plugins/i18n"
import {
  checkRegistrationStatus,
  loginOrFlushStore,
  initPrograms,
  flushPagination,
  flushToken,
  PopulateConsumerData,
  PopulateCoordinatorData,
} from "./guards"
import Welcome from "../layouts/Welcome.vue"
import ManagementDashboard from "../layouts/ManagementDashboard.vue"
import StudentDashboard from "../layouts/StudentDashboard.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import Profile from "../views/Profile.vue"
import ConsumerProfile from "../views/ConsumerProfile.vue"
import SchoolDetails from "../views/SchoolDetails.vue"
import ProgramsExplorer from "../views/ProgramsExplorer/ProgramsExplorer.vue"
import Invite from "../views/Invite/Invite.vue"
import ResetPassword from "../views/ResetPassword.vue"
import GenericError from "../views/Error.vue"
import ProgramModal from "../views/ProgramModal"

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
            path: "reset-password/:userType/:uid/:token",
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
            component: ProgramsExplorer,
            beforeEnter: initPrograms,
            children: [
              {
                path: "program-modal/:slug",
                component: ProgramModal,
                props: true,
              },
            ],
          },
        ]
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
                component: ProgramModal,
                props: true,
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
