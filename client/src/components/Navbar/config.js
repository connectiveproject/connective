import Vue from "vue"
import EventBus from "../../helpers/eventBus"
import i18n from "../../plugins/i18n"
import store from "../../vuex/store"

const coordinatorTabs = [
  {
    text: i18n.t("myActivity.activeGroups"),
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
    text: i18n.t("events.eventsBoard"),
    componentName: "MyEvents",
    icon: "mdi-calendar-heart",
  },
  {
    text: i18n.t("myActivity.students"),
    componentName: "ConsumerList",
    icon: "mdi-account-group",
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
    text: i18n.t("myActivity.activeGroups"),
    componentName: "ConsumerMyGroups",
    icon: "mdi-home-group",
  },
  {
    text: i18n.t("events.eventsBoard"),
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
    id: "events-approve-navbar-tab",
    text: i18n.t("events.requestsForEvents"),
    componentName: "VendorEventsApprove",
    icon: "mdi-email-newsletter",
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
    id: "help-navbar-btn",
    text: i18n.t("general.pageExplanation"),
    icon: "mdi-help-rhombus",
    onClick: () => EventBus.$emit("triggerIntro"),
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
    onClick: () => EventBus.$emit("triggerIntro"),
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
    onClick: () => EventBus.$emit("triggerIntro"),
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
    onClick: () => EventBus.$emit("triggerIntro"),
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
