<template>
  <div>
    <v-toolbar dark prominent :src="bg">
      <v-app-bar-nav-icon
        v-if="$vuetify.breakpoint.mobile"
        @click="mobileDrawer = true"
      />
      <v-toolbar-title
        class="px-md-6"
        :class="{ absolute: $vuetify.breakpoint.mobile }"
        v-text="$t('general.connective')"
      />
      <v-spacer />
      <div class="px-md-6 align-self-center">
        <account-menu
          :avatar-options="profile.profilePicture"
          :name="userDetails.name"
          :email="userDetails.email"
          :buttons="accountButtons"
        />
      </div>
      <template v-if="!$vuetify.breakpoint.mobile" v-slot:extension>
        <route-tabs :tabs="tabs" color="primary" class="px-md-6" />
      </template>
    </v-toolbar>

    <v-navigation-drawer
      v-if="$vuetify.breakpoint.mobile"
      v-model="mobileDrawer"
      disable-resize-watcher
      disable-route-watcher
      app right
    >
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title v-text="$t('general.connective')" />
            <v-list-item-subtitle v-text="$t('general.navigationMenu')" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider />

      <v-list nav dense>
        <v-list-item-group
          v-model="group"
          active-class=""
        >
          <v-list-item
            v-for="tab in tabs"
            :key="tab.id"
            @click="$router.push({ name: tab.componentName })"
          >
            <v-list-item-icon>
              <v-icon v-text="tab.icon" color="primary" />
            </v-list-item-icon>
            <v-list-item-title> {{ tab.text }} </v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState } from "vuex"
import { BACKGROUNDS } from "../../helpers/constants/images"
import { userToTabs, userToAccountButtons } from "./config"
import AccountMenu from "../AccountMenu"
import RouteTabs from "../RouteTabs"

export default {
  components: { AccountMenu, RouteTabs },
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
      group: null,
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
