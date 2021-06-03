<template>
  <v-toolbar dark prominent :src="bg">
    <v-tooltip v-for="btn in buttons" :key="btn.id" bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on" @click="btn.onClick">
          <v-icon>{{ btn.icon }}</v-icon>
        </v-btn>
      </template>
      <span> {{ btn.text() }} </span>
    </v-tooltip>
    <v-toolbar-title :class="{ absolute: $vuetify.breakpoint.mobile }">{{
      $t("general.connective")
    }}</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-app-bar-nav-icon></v-app-bar-nav-icon>
  </v-toolbar>
</template>

<script>
import { mapActions } from "vuex"
import { backgrounds } from "../../helpers/constants/images"

export default {
  data() {
    const buttons = [
      {
        text: () => this.$t("auth.logout"),
        icon: "mdi-export",
        onClick: () => this.logout(),
      },
      {
        text: () => this.$t("general.profile"),
        icon: "mdi-account",
        onClick: () => this.$router.push({ name: "Profile" }),
      },
      {
        text: () => this.$tc("general.school", 0),
        icon: "mdi-home",
        onClick: () => this.$router.push({ name: "SchoolDetails" }),
      },
      {
        text: () => this.$t("invite.usersInvitation"),
        icon: "mdi-account-multiple-plus",
        onClick: () => this.$router.push({ name: "Invite" }),
      },
      {
        text: () => this.$tc("general.program", 1),
        icon: "mdi-handshake",
        onClick: () => this.$router.push({ name: "ProgramsExplorer" }),
      },
    ]
    return {
      bg: backgrounds.navbar,
      buttons,
    }
  },

  methods: {
    ...mapActions("auth", ["logout"]),
  },
}
</script>
