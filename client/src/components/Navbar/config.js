import Vue from "vue"
import i18n from "@/plugins/i18n"
import store from "@/vuex/store"

const coordinatorTabs = [
  {
    text: i18n.t("myActivity.myGroups"),
    componentName: "MyGroups",
    icon: "mdi-home-group",
  },
  {
    id: "program-explorer-navbar-tab",
    text: i18n.tc("general.program", 1),
    componentName: "ProgramsExplorer",
    icon: "mdi-handshake",
  },
  {
    id: "events-navbar-btn",
    text: i18n.t("events.eventsSummary"),
    componentName: "CoordinatorEvents",
    icon: "mdi-file-table-box-multiple-outline",
  },
  {
    text: i18n.t("posts.myFeed"),
    componentName: "CoordinatorEventFeedView",
    icon: "mdi-comment-quote",
  },
  {
    text: i18n.t("myActivity.statistics"),
    componentName: "CoordinatorStatistics",
    icon: "mdi-chart-areaspline",
  },
]

const consumerTabs = [
  {
    id: "program-explorer-navbar-tab",
    text: i18n.tc("general.program", 1),
    componentName: "ConsumerProgramsExplorer",
    icon: "mdi-handshake",
  },
  {
    text: i18n.t("myActivity.myGroups"),
    componentName: "ConsumerMyGroups",
    icon: "mdi-home-group",
  },
  {
    text: i18n.t("events.eventsCalendar"),
    componentName: "ConsumerMyEvents",
    icon: "mdi-calendar-heart",
  },
  {
    text: i18n.t("events.eventsFeedback"),
    componentName: "ConsumerPendingEventsFeedback",
    icon: "mdi-file-document-edit",
  },
]

const instructorTabs = [
  {
    id: "events-summary-navbar-tab",
    text: i18n.t("events.eventsSummary"),
    componentName: "InstructorUnsummarizedEvents",
    icon: "mdi-file-document-edit",
  },
  {
    text: i18n.t("posts.myFeed"),
    componentName: "InstructorEventFeedView",
    icon: "mdi-comment-quote",
  },
]

const vendorTabs = [
  {
    id: "my-programs-navbar-tab",
    text: i18n.t("myActivity.myPrograms"),
    componentName: "VendorProgramList",
    icon: "mdi-handshake",
  },
  {
    id: "events-groups-navbar-tab",
    text: i18n.t("myActivity.myGroups"),
    componentName: "VendorGroupsTable",
    icon: "mdi-home-group",
  },
  {
    id: "events-approve-navbar-tab",
    text: i18n.t("events.requestsForEvents"),
    componentName: "VendorEventsApprove",
    icon: "mdi-email-newsletter",
  },
  {
    id: "events-navbar-btn",
    text: i18n.t("events.eventsSummary"),
    componentName: "VendorEvents",
    icon: "mdi-file-table-box-multiple-outline",
  },
]

const coordinatorAccountButtons = [
  {
    id: "profile-navbar-btn",
    text: i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "CoordinatorProfile" }),
  },
  // Add "Notification" menu entry - not fully implementes yet
  // {
  //   id: "notifications-navbar-btn",
  //   text: i18n.t("notifications.notificationMenuTitle"),
  //   icon: "mdi-bell",
  //   alert: VUEX_STATE.notificationHasNew,
  //   onClick: () => store.dispatch("notification/setVisible", true),
  // },
  {
    id: "school-detail-navbar-btn",
    text: i18n.tc("general.school", 0),
    icon: "mdi-home",
    onClick: () => Vue.$router.push({ name: "SchoolDetails" }),
  },

  {
    id: "help-navbar-btn",
    text: i18n.t("general.pageExplanation"),
    icon: "mdi-help-rhombus",
    onClick: () => store.dispatch("introjs/triggerIntro"),
  },
  {
    id: "logout-navbar-btn",
    text: i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
]

const consumerAccountButtons = [
  {
    id: "profile-navbar-btn",
    text: i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "ConsumerProfile" }),
  },
  {
    id: "help-navbar-btn",
    text: i18n.t("general.pageExplanation"),
    icon: "mdi-help-rhombus",
    onClick: () => store.dispatch("introjs/triggerIntro"),
  },
  {
    id: "logout-navbar-btn",
    text: i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
]

const instructorAccountButtons = [
  {
    id: "profile-navbar-btn",
    text: i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "InstructorProfile" }),
  },
  {
    id: "help-navbar-btn",
    text: i18n.t("general.pageExplanation"),
    icon: "mdi-help-rhombus",
    onClick: () => store.dispatch("introjs/triggerIntro"),
  },
  {
    id: "logout-navbar-btn",
    text: i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
]

const vendorAccountButtons = [
  {
    id: "profile-navbar-btn",
    text: i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "VendorProfile" }),
  },
  {
    id: "user-invite-navbar-btn",
    text: i18n.t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    onClick: () => Vue.$router.push({ name: "OrganizationInviteWrapper" }),
  },
  {
    id: "help-navbar-btn",
    text: i18n.t("general.pageExplanation"),
    icon: "mdi-help-rhombus",
    onClick: () => store.dispatch("introjs/triggerIntro"),
  },
  {
    id: "logout-navbar-btn",
    text: i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
]

const supervisorAccountButtons = [
  {
    id: "profile-navbar-btn",
    text: i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "SupervisorProfile" }),
  },
  {
    id: "help-navbar-btn",
    text: i18n.t("general.pageExplanation"),
    icon: "mdi-help-rhombus",
    onClick: () => store.dispatch("introjs/triggerIntro"),
  },
  {
    id: "logout-navbar-btn",
    text: i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
]


export const userToTabs = {
  consumer: consumerTabs,
  coordinator: coordinatorTabs,
  instructor: instructorTabs,
  vendor: vendorTabs,
  supervisor: []
}

export const userToAccountButtons = {
  consumer: consumerAccountButtons,
  coordinator: coordinatorAccountButtons,
  instructor: instructorAccountButtons,
  vendor: vendorAccountButtons,
  supervisor: supervisorAccountButtons,
}

// tabs that are visible according to user privileges:
export let allTabs = [
  {
    text: i18n.t("myActivity.students"),
    componentName: "ConsumerList",
    icon: "mdi-account-group",
    privileges: ["PRIV_USER_CONSUMER_VIEW", "PRIV_USER_CONSUMER_EDIT"],
  },
  {
    text: i18n.t("events.eventsCalendar"),
    componentName: "MyEvents",
    icon: "mdi-calendar-heart",
    privileges: ["PRIV_EVENT_VIEW", "PRIV_EVENT_EDIT", "PRIV_EVENT_EDIT_MY_ONLY"],
  },
]

export let accountMenuItems = [
  {
    id: "user-invite-navbar-btn",
    text: i18n.t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    privileges: ["PRIV_USER_CONSUMER_VIEW", "PRIV_USER_CONSUMER_EDIT"],
    onClick: () => Vue.$router.push({ name: "SchoolInviteWrapper" }),
  },
]
