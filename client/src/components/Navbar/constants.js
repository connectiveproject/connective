import vm from "../../main.js"
import store from "../../vuex/store"

const coordinatorButtons = [
  {
    text: () => vm.$t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    text: () => vm.$t("general.profile"),
    icon: "mdi-account",
    onClick: () => vm.$router.push({ name: "Profile" }),
  },
  {
    text: () => vm.$tc("general.school", 0),
    icon: "mdi-home",
    onClick: () => vm.$router.push({ name: "SchoolDetails" }),
  },
  {
    text: () => vm.$t("invite.usersInvitation"),
    icon: "mdi-account-multiple-plus",
    onClick: () => vm.$router.push({ name: "Invite" }),
  },
  {
    text: () => vm.$tc("general.program", 1),
    icon: "mdi-handshake",
    onClick: () => vm.$router.push({ name: "ProgramsExplorer" }),
  },
]

const consumerButtons = [
  {
    text: () => vm.$t("auth.logout"),
    icon: "mdi-export",
    onClick: () => store.dispatch("auth/logout"),
  },
  {
    text: () => vm.$t("general.profile"),
    icon: "mdi-account",
    onClick: () => vm.$router.push({ name: "ConsumerProfile" }),
  },
]

export const userToButtons = {
  consumer: consumerButtons,
  coordinator: coordinatorButtons,
}
