import Vue from "vue"
import i18n from "../../plugins/i18n"
import store from "../../vuex/store"

const coordinatorButtons = [
  {
    text: i18n.t("myActivity.activeGroups"),
    componentName: "MyGroups",
  },
  {
    id: "program-explorer-navbar-btn",
    text: i18n.tc("general.program", 1),
    componentName: "ProgramsExplorer",
  },
  {
    text: i18n.t("events.eventsSummary"),
    componentName: "CoordinatorEventFeedView",
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
    text: i18n.t("myActivity.statistics"),
    componentName: "CoordinatorStatistics",
  },
]

const consumerButtons = [
  {
    id: "logout-navbar-btn",
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    id: "profile-navbar-btn",
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "ConsumerProfile" }),
  },
  {
    id: "program-explorer-navbar-btn",
    text: () => i18n.tc("general.program", 1),
    icon: "mdi-handshake",
    onClick: () => Vue.$router.push({ name: "ConsumerProgramsExplorer" }),
  },
  {
    id: "my-activity-navbar-btn",
    text: () => i18n.tc("myActivity.myActivity"),
    icon: "mdi-drawing",
    onClick: () => Vue.$router.push({ name: "ConsumerMyActivity" }),
  },
]

const instructorButtons = [
  {
    id: "logout-navbar-btn",
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    id: "profile-navbar-btn",
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "InstructorProfile" }),
  },
  {
    id: "events-summary-navbar-btn",
    text: () => i18n.t("events.eventsSummary"),
    icon: "mdi-newspaper-variant",
    onClick: () => Vue.$router.push({ name: "InstructorUnsummarizedEvents" }),
  },
  {
    text: () => i18n.t("events.eventsSummary"),
    icon: "mdi-comment-quote",
    onClick: () => Vue.$router.push({ name: "InstructorEventFeedView" }),
  },
]

const vendorButtons = [
  {
    id: "logout-navbar-btn",
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    id: "profile-navbar-btn",
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "VendorProfile" }),
  },
  {
    id: "user-invite-navbar-btn",
    text: () => i18n.t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    onClick: () => Vue.$router.push({ name: "OrganizationInviteWrapper" }),
  },
  {
    id: "my-programs-navbar-btn",
    text: () => i18n.t("myActivity.myPrograms"),
    icon: "mdi-handshake",
    onClick: () => Vue.$router.push({ name: "VendorProgramList" }),
  },
  {
    id: "events-approve-navbar-btn",
    text: () => i18n.t("events.requestsForEvents"),
    icon: "mdi-email-newsletter ",
    onClick: () => Vue.$router.push({ name: "VendorEventsApprove" }),
  },
]

const coordinatorAccountButtons = [
  {
    id: "profile-navbar-btn",
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "CoordinatorProfile" }),
  },
  {
    id: "school-detail-navbar-btn",
    text: () => i18n.tc("general.school", 0),
    icon: "mdi-home",
    onClick: () => Vue.$router.push({ name: "SchoolDetails" }),
  },
  {
    id: "user-invite-navbar-btn",
    text: () => i18n.t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    onClick: () => Vue.$router.push({ name: "SchoolInviteWrapper" }),
  },
  {
    id: "logout-navbar-btn",
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
]

export const userToButtons = {
  consumer: consumerButtons,
  coordinator: coordinatorButtons,
  instructor: instructorButtons,
  vendor: vendorButtons,
}

export const userToAccountButtons = {
  coordinator: coordinatorAccountButtons,
}
