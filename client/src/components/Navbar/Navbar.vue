<template>
  <div>
    <v-toolbar dark prominent :src="bg">
      <v-app-bar-nav-icon
        v-if="$vuetify.breakpoint.xs"
        introjs="navigation"
        @click="mobileDrawer = true"
      />
      <v-toolbar-title
        class="px-md-6"
        :class="{ absolute: $vuetify.breakpoint.xs }"
        v-text="$t('general.connective')"
      />
      <v-spacer />
      <div class="px-md-6 align-self-center" introjs="navbar-account-menu">
        <account-menu
          :avatar-options="profile.profilePicture"
          :name="userDetails.name"
          :email="userDetails.email"
          :buttons="accountButtons"
        />
      </div>
      <template v-if="!$vuetify.breakpoint.xs" v-slot:extension>
        <route-tabs
          :tabs="tabs"
          color="primary"
          class="px-6"
        />
      </template>
    </v-toolbar>
    <navigation-drawer
      v-if="$vuetify.breakpoint.xs"
      v-model="mobileDrawer"
      :nav-items="tabs"
      :title="$t('general.connective')"
      :subtitle="$t('general.navigationMenu')"
      disable-resize-watcher
      disable-route-watcher
    />
  </div>
</template>

<script>
import { mapState } from "vuex"
import { BACKGROUNDS } from "../../helpers/constants/images"
import { userToTabs, userToAccountButtons } from "./config"
import AccountMenu from "../AccountMenu"
import RouteTabs from "../RouteTabs"
import NavigationDrawer from "../NavigationDrawer"

export default {
  components: { AccountMenu, RouteTabs, NavigationDrawer },
  props: {
    userType: {
      type: String,
      required: true,
      validator(value) {
        return ["coordinator", "consumer", "instructor", "vendor"].includes(
          value
        )
      },
    },
  },
  data() {
    return {
      mobileDrawer: false,
      bg: BACKGROUNDS.navbar,
      tabs: userToTabs[this.userType],
      accountButtons: userToAccountButtons[this.userType],
    }
  },
  computed: {
    ...mapState("user", ["userDetails"]),
    profile() {
      return this.$store.state[this.userType].profile
    },
  },
}
</script>
