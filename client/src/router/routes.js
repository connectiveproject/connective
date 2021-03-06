import i18n from "@/plugins/i18n"
import guards, { chainGuards } from "@/router/guards"
import Welcome from "@/layouts/Welcome"
import GeneralDashboard from "@/layouts/GeneralDashboard"
import CoordinatorDashboard from "@/layouts/CoordinatorDashboard"
import StudentDashboard from "@/layouts/StudentDashboard"
import InstructorDashboard from "@/layouts/InstructorDashboard"
import VendorDashboard from "@/layouts/VendorDashboard"
import SupervisorDashboard from "@/layouts/SupervisorDashboard"
import Login from "@/views/Login"
import CoordinatorRegister from "@/views/Register/CoordinatorRegister"
import VendorRegister from "@/views/Register/VendorRegister"
import CoordinatorProfile from "@/views/Profile/CoordinatorProfile"
import EventSummaryList from "@/views/EventSummaryList"
import ConsumerProfile from "@/views/Profile/ConsumerProfile"
import InstructorProfile from "@/views/Profile/InstructorProfile"
import VendorProfile from "@/views/Profile/VendorProfile"
import SupervisorProfile from "@/views/Profile/SupervisorProfile"
import SchoolDetails from "@/views/SchoolDetails"
import EventFeedView from "@/views/EventFeedView"
import ProgramsExplorer from "@/views/ProgramsExplorer/ProgramsExplorer"
import ConsumerProgramsExplorer from "@/views/ProgramsExplorer/ConsumerProgramsExplorer"
import SchoolInviteWrapper from "@/views/Invite/SchoolInviteWrapper"
import OrganizationInviteWrapper from "@/views/Invite/OrganizationInviteWrapper"
import InviteConsumers from "@/views/Invite/InviteConsumers"
import InviteCoordinators from "@/views/Invite/InviteCoordinators"
import InviteInstructors from "@/views/Invite/InviteInstructors"
import InviteVendors from "@/views/Invite/InviteVendors"
import ResetPassword from "@/views/ResetPassword"
import RecoverPassword from "@/views/RecoverPassword"
import GenericError from "@/views/Error"
import ProgramModal from "@/views/ProgramModal"
import MyGroups from "@/views/MyGroups/MyGroups"
import ConsumerMyGroups from "@/views/MyGroups/ConsumerMyGroups"
import MyEvents from "@/views/MyEvents/MyEvents"
import CoordinatorEventCreator from "@/views/CoordinatorEventCreator"
import ConsumerList from "@/views/ConsumerList/ConsumerList"
import ConsumerMyEvents from "@/views/MyEvents/ConsumerMyEvents"
import ConsumerPendingEventsFeedback from "@/views/ConsumerPendingEventsFeedback"
import ConsumerEventFeedback from "@/views/ConsumerEventFeedback"
import CoordinatorStatistics from "@/views/CoordinatorStatistics"
import InstructorUnsummarizedEvents from "@/views/InstructorUnsummarizedEvents"
import InstructorEventSummary from "@/views/InstructorEventSummary"
import GroupEditor from "@/views/GroupEditor"
import CreateGroup from "@/views/CreateGroup"
import AssignGroupConsumers from "@/views/AssignGroupConsumers"
import GroupDetail from "@/views/GroupDetail"
import VendorProgramList from "@/views/VendorProgramList"
import VendorGroupsTable from "@/views/VendorGroupsTable"
import VendorDetailProgram from "@/views/VendorDetailProgram"
import VendorProgramMediaUpload from "@/views/VendorProgramMediaUpload"
import VendorProgramCreator from "@/views/VendorProgramCreator"
import VendorEventsApprove from "@/views/VendorEventsApprove"
import VendorMyEvents from "@/views/MyEvents/VendorMyEvents"
import CoordinatorEventOrderStatus from "@/views/CoordinatorEventOrderStatus"


let connectiveRoutes = [
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
            props: true,
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
        name: "SupervisorDashboard",
        redirect: { name: "SupervisorProfile" },
        component: SupervisorDashboard,
        beforeEnter: chainGuards([guards.supervisorOnly, guards.populateSupervisorData]),
        children: [
          {
            path: "profile",
            name: "SupervisorProfile",
            component: SupervisorProfile,
          },
        ],
      },
      {
        path: "student-dashboard",
        name: "StudentDashboard",
        redirect: { name: "ConsumerProfile" },
        component: StudentDashboard,
        beforeEnter: chainGuards([guards.consumerOnly, guards.populateConsumerData]),
        children: [
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
        name: "CoordinatorDashboard",
        redirect: { name: "CoordinatorProfile" },
        beforeEnter: chainGuards([guards.coordOnly, guards.populateCoordinatorData]),
        children: [
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
        name: "InstructorDashboard",
        redirect: { name: "InstructorProfile" },
        beforeEnter: chainGuards([guards.instructorOnly, guards.populateInstructorData]),
        children: [
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
        name: "VendorDashboard",
        redirect: { name: "VendorProgramList" },
        beforeEnter: chainGuards([guards.vendorOnly, guards.populateVendorData]),
        children: [
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
            path: "my-events",
            name: "VendorMyEvents",
            component: VendorMyEvents,
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
          {
            path: "events",
            name: "VendorEvents",
            component: EventSummaryList,
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
        path: "mp",
        component: GeneralDashboard,
        name: "GeneralDashboard",
        beforeEnter: chainGuards([guards.populateUserData]),
        children: [],
      },
    ],
  },
  {
    path: "*",
    redirect: "/",
  },
]

// Routes that are not user-type specific. New routes should be added here:
let generalChildrenRoutes = [
  {
    path: "student-list",
    name: "ConsumerList",
    component: ConsumerList,
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
    path: "my-events",
    name: "MyEvents",
    component: MyEvents,
  },
  {
    path: "events",
    name: "CoordinatorEvents",
    component: EventSummaryList,
  },
  {
    path: "event-creator",
    name: "CoordinatorEventCreator",
    component: CoordinatorEventCreator,
    props: true,
  },
]

export function addChildToComponent(routes, componentName, childToAdd) {
  const component = routes.children.find(r => r.name === componentName)
  if (!component) {
    // couldn't find the child component:
    throw new Error(`Cannot find component: ${componentName}`)
  }
  component.children.push(childToAdd)
}

// embed the general routes into the main routes:
for (const child of generalChildrenRoutes) {
  addChildToComponent(connectiveRoutes[1], "GeneralDashboard", child)
}

export default connectiveRoutes
