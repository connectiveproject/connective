import i18n from "../plugins/i18n"
import guards, { chainGuards } from "@/router/guards"
import Welcome from "../layouts/Welcome"
import CoordinatorDashboard from "../layouts/CoordinatorDashboard"
import StudentDashboard from "../layouts/StudentDashboard"
import InstructorDashboard from "../layouts/InstructorDashboard"
import VendorDashboard from "../layouts/VendorDashboard"
import SupervisorDashboard from "../layouts/SupervisorDashboard"
import Login from "../views/Login"
import CoordinatorRegister from "../views/Register/CoordinatorRegister"
import VendorRegister from "../views/Register/VendorRegister"
import CoordinatorProfile from "../views/Profile/CoordinatorProfile"
import ConsumerProfile from "../views/Profile/ConsumerProfile"
import InstructorProfile from "../views/Profile/InstructorProfile"
import VendorProfile from "../views/Profile/VendorProfile"
import SupervisorProfile from "../views/Profile/SupervisorProfile"
import SchoolDetails from "../views/SchoolDetails"
import EventFeedView from "../views/EventFeedView"
import ProgramsExplorer from "../views/ProgramsExplorer/ProgramsExplorer"
import ConsumerProgramsExplorer from "../views/ProgramsExplorer/ConsumerProgramsExplorer"
import SchoolInviteWrapper from "../views/Invite/SchoolInviteWrapper"
import OrganizationInviteWrapper from "../views/Invite/OrganizationInviteWrapper"
import InviteConsumers from "../views/Invite/InviteConsumers"
import InviteCoordinators from "../views/Invite/InviteCoordinators"
import InviteInstructors from "../views/Invite/InviteInstructors"
import InviteVendors from "../views/Invite/InviteVendors"
import ResetPassword from "../views/ResetPassword"
import RecoverPassword from "../views/RecoverPassword"
import GenericError from "../views/Error"
import ProgramModal from "../views/ProgramModal"
import MyGroups from "../views/MyGroups/MyGroups"
import ConsumerMyGroups from "../views/MyGroups/ConsumerMyGroups"
import MyEvents from "../views/MyEvents/MyEvents"
import CoordinatorEventCreator from "../views/CoordinatorEventCreator"
import ConsumerList from "../views/ConsumerList/ConsumerList"
import ConsumerMyEvents from "../views/MyEvents/ConsumerMyEvents"
import ConsumerPendingEventsFeedback from "../views/ConsumerPendingEventsFeedback"
import ConsumerEventFeedback from "../views/ConsumerEventFeedback"
import CoordinatorStatistics from "../views/CoordinatorStatistics"
import InstructorUnsummarizedEvents from "../views/InstructorUnsummarizedEvents"
import InstructorEventSummary from "../views/InstructorEventSummary"
import GroupEditor from "../views/GroupEditor"
import CreateGroup from "../views/CreateGroup"
import AssignGroupConsumers from "../views/AssignGroupConsumers"
import GroupDetail from "../views/GroupDetail"
import VendorProgramList from "../views/VendorProgramList"
import VendorGroupsTable from "../views/VendorGroupsTable"
import VendorDetailProgram from "../views/VendorDetailProgram"
import VendorProgramMediaUpload from "../views/VendorProgramMediaUpload"
import VendorProgramCreator from "../views/VendorProgramCreator"
import VendorEventsApprove from "../views/VendorEventsApprove"
import CoordinatorEventOrderStatus from "../views/CoordinatorEventOrderStatus"


export default [
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
        children: [
          {
            path: "school-staff-register",
            name: "CoordinatorRegister",
            component: CoordinatorRegister,
            beforeEnter: guards.loginIfSignupComplete,
            props: true,
          },
          {
            path: "vendor-register",
            name: "VendorRegister",
            component: VendorRegister,
            beforeEnter: guards.loginIfSignupComplete,
          },
          {
            path: "recover-password",
            name: "RecoverPassword",
            component: RecoverPassword,
            beforeEnter: guards.loginIfAuthenticated,
          },
          {
            path: "reset-password/:mode/:uid/:token",
            name: "ResetPassword",
            component: ResetPassword,
            beforeEnter: guards.loginIfAuthenticated,
            props: true,
          },
          {
            path: "login",
            name: "Login",
            component: Login,
            beforeEnter: guards.loginIfAuthenticated,
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
        beforeEnter: guards.checkRegistrationStatus,
      },
      {
        path: "supervisor-dashboard",
        component: SupervisorDashboard,
        beforeEnter: chainGuards([guards.supervisorOnly, guards.populateSupervisorData]),
        children: [
          {
            path: "",
            name: "SupervisorDashboard",
            redirect: { name: "SupervisorProfile" },
          },
          {
            path: "profile",
            name: "SupervisorProfile",
            component: SupervisorProfile,
          },
        ],
      },
      {
        path: "student-dashboard",
        component: StudentDashboard,
        beforeEnter: chainGuards([guards.consumerOnly, guards.populateConsumerData]),
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
            beforeEnter: guards.initConsumerPrograms,
            children: [
              {
                path: "program-modal/:slug",
                name: "ConsumerProgramModal",
                component: ProgramModal,
                beforeEnter: guards.fetchProgramDetails,
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
        beforeEnter: chainGuards([guards.coordOnly, guards.populateCoordinatorData]),
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
              },
              {
                path: "invite-staff",
                name: "InviteCoordinators",
                component: InviteCoordinators,
              },
            ],
          },
          {
            path: "programs-explorer",
            name: "ProgramsExplorer",
            component: ProgramsExplorer,
            beforeEnter: guards.initPrograms,
            children: [
              {
                path: "program-modal/:slug",
                name: "ProgramModal",
                component: ProgramModal,
                beforeEnter: guards.fetchProgramDetails,
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
        beforeEnter: chainGuards([guards.instructorOnly, guards.populateInstructorData]),
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
          },
        ],
      },
      {
        path: "vendor-dashboard",
        component: VendorDashboard,
        beforeEnter: chainGuards([guards.vendorOnly, guards.populateVendorData]),
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
              },
              {
                path: "invite-vendors",
                name: "InviteVendors",
                component: InviteVendors,
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
