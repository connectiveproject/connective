import Vue from "vue"
import i18n from "../../plugins/i18n"
import store from "../../vuex/store"

const coordinatorTabs = [
  {
    text: i18n.t("myActivity.activeGroups"),
    componentName: "MyGroups",
  },
  {
    id: "program-explorer-navbar-tab",
    text: i18n.tc("general.program", 1),
    componentName: "ProgramsExplorer",
  },
  {
    text: i18n.t("events.eventsBoard"),
    componentName: "MyEvents",
  },
  {
    text: i18n.t("myActivity.students"),
    componentName: "ConsumerList",
  },
  {
    text: i18n.t("posts.myFeed"),
    componentName: "CoordinatorEventFeedView",
  },
  {
    text: i18n.t("myActivity.statistics"),
    componentName: "CoordinatorStatistics",
  },
]

const consumerTabs = [
  {
    id: "program-explorer-navbar-tab",
    text: i18n.tc("general.program", 1),
    componentName: "ConsumerProgramsExplorer",
  },
  {
    text: i18n.t("myActivity.activeGroups"),
    componentName: "ConsumerMyGroups",
  },
  {
    text: i18n.t("events.eventsBoard"),
    componentName: "ConsumerMyEvents",
  },
  {
    text: i18n.t("events.eventsFeedback"),
    componentName: "ConsumerPendingEventsFeedback",
  },
]

const instructorTabs = [
  {
    id: "events-summary-navbar-tab",
    text: i18n.t("events.eventsSummary"),
    componentName: "InstructorUnsummarizedEvents",
  },
  {
    text: i18n.t("posts.myFeed"),
    componentName: "InstructorEventFeedView",
  },
]

const vendorTabs = [
  {
    id: "my-programs-navbar-tab",
    text: i18n.t("myActivity.myPrograms"),
    componentName: "VendorProgramList",
  },
  {
    id: "events-approve-navbar-tab",
    text: i18n.t("events.requestsForEvents"),
    componentName: "VendorEventsApprove",
  },
]

const coordinatorAccountButtons = [
  {
    id: "profile-navbar-btn",
    text: i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "CoordinatorProfile" }),
  },
  {
    id: "school-detail-navbar-btn",
    text: i18n.tc("general.school", 0),
    icon: "mdi-home",
    onClick: () => Vue.$router.push({ name: "SchoolDetails" }),
  },
  {
    id: "user-invite-navbar-btn",
    text: i18n.t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    onClick: () => Vue.$router.push({ name: "SchoolInviteWrapper" }),
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
}

export const userToAccountButtons = {
  consumer: consumerAccountButtons,
  coordinator: coordinatorAccountButtons,
  instructor: instructorAccountButtons,
  vendor: vendorAccountButtons,
}
