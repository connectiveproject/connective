<template>
  <div>
    <v-toolbar dark prominent>
      <template slot="img">
        <v-img style="filter: brightness(65%)" :src="bg" height="300" />
      </template>
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
      <div
        class="px-md-6 align-self-center"
        introjs="navbar-account-menu"
        data-testid="navbar-account-menu"
      >
        <account-menu
          :avatar-options="profile.profilePicture"
          :name="userDetails.name"
          :email="userDetails.email"
          :buttons="accountButtons"
        />
      </div>
      <template v-if="!$vuetify.breakpoint.xs" v-slot:extension>
        <route-tabs :tabs="tabs" color="primary" class="px-6" />
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
    <notifications-list
      v-if="notificationsVisible"
      v-model="notificationsVisible"
    />
  </div>
</template>

<script>
import { mapState } from "vuex"

import { BACKGROUNDS } from "@/helpers/constants/images"
import {
  userToTabs,
  userToAccountButtons,
  allTabs,
} from "@/components/Navbar/config"
import AccountMenu from "@/components/AccountMenu"
import RouteTabs from "@/components/RouteTabs"
import NavigationDrawer from "@/components/NavigationDrawer"
import NotificationsList from "@/components/Navbar/NotificationsList.vue"
export default {
  components: {
    AccountMenu,
    RouteTabs,
    NavigationDrawer,
    NotificationsList,
  },

  props: {
    userType: {
      type: String,
      required: true,
      validator(value) {
        return Object.keys({ ...userToTabs, ...userToAccountButtons }).includes(
          value
        )
      },
    },
  },
  data() {
    return {
      mobileDrawer: false,
      bg: BACKGROUNDS.navbar,

      accountButtons: userToAccountButtons[this.userType],
    }
  },
  computed: {
    ...mapState("user", ["userDetails"]),
    profile() {
      return this.$store.state[this.userType].profile
    },
    notificationsVisible: {
      get() {
        return this.$store.state.notification.visible
      },
      set(newValue) {
        return this.$store.dispatch("notification/setVisible", newValue)
      },
    },
    tabs() {
      const hasPrivilege = privilege => {
        return this.userDetails.privileges.includes(privilege)
      }
      let privilegedTabs = allTabs.filter(tab =>
        tab.privileges.some(hasPrivilege)
      )
      // combine the user-type tabs with the tabs that are accessible by the user's privileges:
      const result = userToTabs[this.userType].concat(privilegedTabs)
      return result
    },
  },
}
</script>
