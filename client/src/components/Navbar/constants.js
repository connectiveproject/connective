import Vue from "vue"
import i18n from "../../plugins/i18n"
import store from "../../vuex/store"

const coordinatorButtons = [
  {
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "CoordinatorProfile" }),
  },
  {
    text: () => i18n.tc("general.school", 0),
    icon: "mdi-home",
    onClick: () => Vue.$router.push({ name: "SchoolDetails" }),
  },
  {
    text: () => i18n.t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    onClick: () => Vue.$router.push({ name: "SchoolInviteWrapper" }),
  },
  {
    text: () => i18n.tc("general.program", 1),
    icon: "mdi-handshake",
    onClick: () => Vue.$router.push({ name: "ProgramsExplorer" }),
  },
  {
    text: () => i18n.tc("myActivity.myActivity"),
    icon: "mdi-drawing",
    onClick: () => Vue.$router.push({ name: "MyActivity" }),
  },
]

const consumerButtons = [
  {
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "ConsumerProfile" }),
  },
  {
    text: () => i18n.tc("general.program", 1),
    icon: "mdi-handshake",
    onClick: () => Vue.$router.push({ name: "ConsumerProgramsExplorer" }),
  },
  {
    text: () => i18n.tc("myActivity.myActivity"),
    icon: "mdi-drawing",
    onClick: () => Vue.$router.push({ name: "ConsumerMyActivity" }),
  },
]

const instructorButtons = [
  {
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "InstructorProfile" }),
  },
  {
    text: () => i18n.t("events.eventsSummary"),
    icon: "mdi-newspaper-variant",
    onClick: () => Vue.$router.push({ name: "InstructorUnsummarizedEvents" }),
  },
]

const vendorButtons = [
  {
    text: () => i18n.t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    text: () => i18n.t("general.profile"),
    icon: "mdi-account",
    onClick: () => Vue.$router.push({ name: "VendorProfile" }),
  },
  {
    text: () => i18n.t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    onClick: () => Vue.$router.push({ name: "OrganizationInviteWrapper" }),
  },
  {
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
