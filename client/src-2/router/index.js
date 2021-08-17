import Vue from "vue"
import VueRouter from "vue-router"
import i18n from "../../src/plugins/i18n"
import {
  checkRegistrationStatus,
  flushState,
  loginIfAuthenticated,
  initPrograms,
  initConsumerPrograms,
  flushPagination,
  flushToken,
  populateConsumerData,
  populateCoordinatorData,
  populateInstructorData,
  populateVendorData,
  fetchProgramDetails,
} from "../../src/router/guards"
import Welcome from "../../src/layouts/Welcome"
import CoordinatorDashboard from "../../src/layouts/CoordinatorDashboard"
import StudentDashboard from "../../src/layouts/StudentDashboard"
import InstructorDashboard from "../../src/layouts/InstructorDashboard"
import VendorDashboard from "../../src/layouts/VendorDashboard"
import Login from "../../src/views/Login"
import CoordinatorRegister from "../../src/views/Register/CoordinatorRegister"
import VendorRegister from "../../src/views/Register/VendorRegister"
import CoordinatorProfile from "../../src/views/Profile/CoordinatorProfile"
import ConsumerProfile from "../../src/views/Profile/ConsumerProfile"
import InstructorProfile from "../../src/views/Profile/InstructorProfile"
import VendorProfile from "../../src/views/Profile/VendorProfile"
import SchoolDetails from "../../src/views/SchoolDetails"
import EventFeedView from "../../src/views/EventFeedView"
import ProgramsExplorer from "../views/ProgramsExplorer"
// import ProgramsExplorer from "../../src/views/ProgramsExplorer/ProgramsExplorer"
import ConsumerProgramsExplorer from "../../src/views/ProgramsExplorer/ConsumerProgramsExplorer"
import SchoolInviteWrapper from "../../src/views/Invite/SchoolInviteWrapper"
import OrganizationInviteWrapper from "../../src/views/Invite/OrganizationInviteWrapper"
import InviteConsumers from "../../src/views/Invite/InviteConsumers"
import InviteCoordinators from "../../src/views/Invite/InviteCoordinators"
import InviteInstructors from "../../src/views/Invite/InviteInstructors"
import InviteVendors from "../../src/views/Invite/InviteVendors"
import ResetPassword from "../../src/views/ResetPassword"
import GenericError from "../../src/views/Error"
import ProgramModal from "../../src/views/ProgramModal"
import MyGroups from "../../src/views/MyGroups/MyGroups"
import ConsumerMyGroups from "../../src/views/MyGroups/ConsumerMyGroups"
import MyEvents from "../../src/views/MyEvents/MyEvents"
import CoordinatorEventCreator from "../../src/views/CoordinatorEventCreator"
import ConsumerList from "../../src/views/ConsumerList/ConsumerList"
import ConsumerMyEvents from "../../src/views/MyEvents/ConsumerMyEvents"
import ConsumerPendingEventsFeedback from "../../src/views/ConsumerPendingEventsFeedback"
import ConsumerEventFeedback from "../../src/views/ConsumerEventFeedback"
import CoordinatorStatistics from "../../src/views/CoordinatorStatistics"
import InstructorUnsummarizedEvents from "../../src/views/InstructorUnsummarizedEvents"
import InstructorEventSummary from "../../src/views/InstructorEventSummary"
import GroupEditor from "../../src/views/GroupEditor"
import CreateGroup from "../../src/views/CreateGroup"
import AssignGroupConsumers from "../../src/views/AssignGroupConsumers"
import GroupDetail from "../../src/views/GroupDetail"
import VendorProgramList from "../../src/views/VendorProgramList"
import VendorGroupsTable from "../../src/views/VendorGroupsTable"
import VendorDetailProgram from "../../src/views/VendorDetailProgram"
import VendorProgramMediaUpload from "../../src/views/VendorProgramMediaUpload"
import VendorProgramCreator from "../../src/views/VendorProgramCreator"
import VendorEventsApprove from "../../src/views/VendorEventsApprove"
import CoordinatorEventOrderStatus from "../../src/views/CoordinatorEventOrderStatus"

Vue.use(VueRouter)

export const routes = [
  {
    path: "/",
    redirect: `/${i18n.locale}/welcome/login`,
  },
  {
    path: "/:lang(he)",
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
        beforeEnter: loginIfAuthenticated,
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
            beforeEnter: flushState,
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
        beforeEnter: populateConsumerData,
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
            path: "my-groups",
            name: "ConsumerMyGroups",
            component: ConsumerMyGroups,
          },
          {
            path: "my-events",
            name: "ConsumerMyEvents",
            component: ConsumerMyEvents,
          },
          {
            path: "events-pending-feedbacks",
            name: "ConsumerPendingEventsFeedback",
            component: ConsumerPendingEventsFeedback,
          },
          {
            path: "event-feedback/:slug",
            name: "ConsumerEventFeedback",
            component: ConsumerEventFeedback,
            props: true,
          },
        ],
      },
      {
        path: "coordinator-dashboard",
        component: CoordinatorDashboard,
        beforeEnter: populateCoordinatorData,
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
            path: "event-feed-view",
            name: "CoordinatorEventFeedView",
            component: EventFeedView,
            beforeEnter: flushPagination,
          },
          {
            path: "schoolDetails",
            name: "SchoolDetails",
            component: SchoolDetails,
          },
          {
            path: "invite",
            component: SchoolInviteWrapper,
            children: [
              {
                path: "",
                name: "SchoolInviteWrapper",
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
            path: "student-list",
            name: "ConsumerList",
            component: ConsumerList,
            beforeEnter: flushPagination,
          },
          {
            path: "statistics",
            name: "CoordinatorStatistics",
            component: CoordinatorStatistics,
          },
          {
            path: "detail-group/:groupSlug",
            name: "GroupDetail",
            component: GroupDetail,
            props: true,
          },
          {
            path: "event-order-status",
            name: "CoordinatorEventOrderStatus",
            component: CoordinatorEventOrderStatus,
          },
          {
            path: "event-creator",
            name: "CoordinatorEventCreator",
            component: CoordinatorEventCreator,
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
        beforeEnter: populateInstructorData,
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
          {
            path: "event-feed-view",
            name: "InstructorEventFeedView",
            component: EventFeedView,
            beforeEnter: flushPagination,
          },
        ],
      },
      {
        path: "vendor-dashboard",
        component: VendorDashboard,
        beforeEnter: populateVendorData,
        children: [
          {
            path: "",
            name: "VendorDashboard",
            redirect: { name: "VendorProgramList" },
          },
          {
            path: "profile",
            name: "VendorProfile",
            component: VendorProfile,
          },
          {
            path: "events-approve",
            name: "VendorEventsApprove",
            component: VendorEventsApprove,
          },
          {
            path: "my-groups",
            name: "VendorGroupsTable",
            component: VendorGroupsTable,
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
          {
            path: "program-creator",
            name: "VendorProgramCreator",
            component: VendorProgramCreator,
          },
          {
            path: "program-media-upload/:programSlug",
            name: "VendorProgramMediaUpload",
            component: VendorProgramMediaUpload,
            props: true,
          },
          {
            path: "invite",
            component: OrganizationInviteWrapper,
            children: [
              {
                path: "",
                name: "OrganizationInviteWrapper",
                redirect: { name: "InviteInstructors" },
              },
              {
                path: "invite-instructors",
                name: "InviteInstructors",
                component: InviteInstructors,
                beforeEnter: flushPagination,
              },
              {
                path: "invite-vendors",
                name: "InviteVendors",
                component: InviteVendors,
                beforeEnter: flushPagination,
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
  {
    path: "*",
    redirect: "/",
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
