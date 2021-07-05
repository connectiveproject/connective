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
import Welcome from "../layouts/Welcome"
import CoordinatorDashboard from "../layouts/CoordinatorDashboard"
import StudentDashboard from "../layouts/StudentDashboard"
import InstructorDashboard from "../layouts/InstructorDashboard"
import VendorDashboard from "../layouts/VendorDashboard"
import MyActivity from "../layouts/MyActivity/MyActivity"
import ConsumerMyActivity from "../layouts/MyActivity/ConsumerMyActivity"
import Login from "../views/Login"
import CoordinatorRegister from "../views/Register/CoordinatorRegister"
import VendorRegister from "../views/Register/VendorRegister"
import CoordinatorProfile from "../views/Profile/CoordinatorProfile"
import ConsumerProfile from "../views/Profile/ConsumerProfile"
import InstructorProfile from "../views/Profile/InstructorProfile"
import VendorProfile from "../views/Profile/VendorProfile"
import SchoolDetails from "../views/SchoolDetails"
import ProgramsExplorer from "../views/ProgramsExplorer/ProgramsExplorer"
import ConsumerProgramsExplorer from "../views/ProgramsExplorer/ConsumerProgramsExplorer"
import Invite from "../views/Invite/Invite"
import InviteConsumers from "../views/Invite/InviteConsumers"
import InviteCoordinators from "../views/Invite/InviteCoordinators"
import ResetPassword from "../views/ResetPassword"
import GenericError from "../views/Error"
import ProgramModal from "../views/ProgramModal"
import MyGroups from "../views/MyGroups/MyGroups"
import ConsumerMyGroups from "../views/MyGroups/ConsumerMyGroups"
import MyEvents from "../views/MyEvents/MyEvents"
import ConsumerMyEvents from "../views/MyEvents/ConsumerMyEvents"
import CoordinatorStatistics from "../views/CoordinatorStatistics"
import InstructorUnsummarizedEvents from "../views/InstructorUnsummarizedEvents"
import InstructorEventSummary from "../views/InstructorEventSummary"
import GroupEditor from "../views/GroupEditor"
import CreateGroup from "../views/CreateGroup"
import AssignGroupConsumers from "../views/AssignGroupConsumers"
import DetailGroup from "../views/DetailGroup"
import VendorProgramList from "../views/VendorProgramList"
import VendorDetailProgram from "../views/VendorDetailProgram/VendorDetailProgram"

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
        path: "",
        redirect: "/",
      },
      {
        path: "welcome",
        name: "Welcome",
        component: Welcome,
        children: [
          {
            path: "school-staff-register",
            name: "CoordinatorRegister",
            component: CoordinatorRegister,
            props: true,
          },
          {
            path: "vendor-register",
            name: "VendorRegister",
            component: VendorRegister,
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
        path: "coordinator-dashboard",
        component: CoordinatorDashboard,
        beforeEnter: PopulateCoordinatorData,
        children: [
          {
            path: "",
            name: "CoordinatorDashboard",
            redirect: { name: "CoordinatorProfile" },
          },
          {
            path: "profile",
            name: "CoordinatorProfile",
            component: CoordinatorProfile,
          },
          {
            path: "schoolDetails",
            name: "SchoolDetails",
            component: SchoolDetails,
          },
          {
            path: "invite",
            component: Invite,
            children: [
              {
                path: "",
                name: "Invite",
                redirect: { name: "InviteConsumers" },
              },
              {
                path: "invite-students",
                name: "InviteConsumers",
                component: InviteConsumers,
                beforeEnter: flushPagination,
              },
              {
                path: "invite-staff",
                name: "InviteCoordinators",
                component: InviteCoordinators,
                beforeEnter: flushPagination,
              },
            ],
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
              {
                path: "statistics",
                name: "CoordinatorStatistics",
                component: CoordinatorStatistics,
              },
            ],
          },
          {
            path: "detail-group/:groupSlug",
            name: "DetailGroup",
            component: DetailGroup,
            props: true,
          },
          {
            path: "group-editor",
            component: GroupEditor,
            children: [
              {
                path: "",
                name: "GroupEditor",
                redirect: { name: "CreateGroup" },
              },
              {
                path: "create-group",
                name: "CreateGroup",
                component: CreateGroup,
              },
              {
                path: "assign-group-students/:groupSlug",
                name: "AssignGroupConsumers",
                component: AssignGroupConsumers,
                props: true,
              },
            ],
          },
        ],
      },
      {
        path: "instructor-dashboard",
        component: InstructorDashboard,
        children: [
          {
            path: "",
            name: "InstructorDashboard",
            redirect: { name: "InstructorProfile" },
          },
          {
            path: "profile",
            name: "InstructorProfile",
            component: InstructorProfile,
          },
          {
            path: "unsummarized-events",
            name: "InstructorUnsummarizedEvents",
            component: InstructorUnsummarizedEvents,
          },
          {
            path: "event-summary/:slug",
            name: "InstructorEventSummary",
            component: InstructorEventSummary,
            props: true,
          },
        ],
      },
      {
        path: "vendor-dashboard",
        component: VendorDashboard,
        children: [
          {
            path: "",
            name: "VendorDashboard",
            redirect: { name: "VendorProfile" },
          },
          {
            path: "profile",
            name: "VendorProfile",
            component: VendorProfile,
          },
          {
            path: "my-programs",
            name: "VendorProgramList",
            component: VendorProgramList,
          },
          {
            path: "detail-program/:programSlug",
            name: "VendorDetailProgram",
            component: VendorDetailProgram,
            props: true,
          },
        ],
      },
      {
        path: "error",
        name: "Error",
        component: GenericError,
        props: true,
      },
      {
        path: "*",
        Name: "PageNotFound",
        component: GenericError,
        props: { bodyKey: "errors.thisPageDoesNotExist" },
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
