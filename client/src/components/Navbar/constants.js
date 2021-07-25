import Vue from "vue"
import i18n from "../../plugins/i18n"
import store from "../../vuex/store"

const coordinatorButtons = [
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
    id: "program-explorer-navbar-btn",
    text: () => i18n.tc("general.program", 1),
    icon: "mdi-handshake",
    onClick: () => Vue.$router.push({ name: "ProgramsExplorer" }),
  },
  {
    id: "my-activity-navbar-btn",
    text: () => i18n.tc("myActivity.myActivity"),
    icon: "mdi-drawing",
    onClick: () => Vue.$router.push({ name: "MyActivity" }),
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
]

export const userToButtons = {
  consumer: consumerButtons,
  coordinator: coordinatorButtons,
  instructor: instructorButtons,
  vendor: vendorButtons,
}
