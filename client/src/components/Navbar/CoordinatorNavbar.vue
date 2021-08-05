<template>
  <v-toolbar dark prominent :src="bg">
    <!-- <v-tooltip v-for="btn in buttons" :key="btn.id" bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          :data-testid="btn.id"
          icon
          v-bind="attrs"
          v-on="on"
          @click="btn.onClick"
        >
          <v-icon v-text="btn.icon" />
        </v-btn>
      </template>
      <span> {{ btn.text() }} </span>
    </v-tooltip> -->
    <v-toolbar-title
      :class="{ absolute: $vuetify.breakpoint.mobile }"
      v-text="$t('general.connective')"
    />
    <v-spacer></v-spacer>
    <account-menu
      :avatar-options="profile.profilePicture"
      :name="userDetails.name"
      :email="userDetails.email"
      :buttons="accountButtons"
    />
    <template v-slot:extension>
      <route-tabs :tabs="buttons" color="primary" />
    </template>
  </v-toolbar>
</template>

<script>
import { mapState } from "vuex"
import store from "../../vuex/store"
import { BACKGROUNDS } from "../../helpers/constants/images"
import { userToButtons, userToAccountButtons } from "./constants"
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
  async beforeRouteEnter(to, from, next) {
    await Promise.all([
      store.dispatch("coordinator/getProfile"),
      store.dispatch("user/getUserDetails"),
    ])
    next()
  },
  data() {
    return {
      bg: BACKGROUNDS.navbar,
      buttons: userToButtons[this.userType],
      accountButtons: userToAccountButtons[this.userType],
    }
  },
  computed: {
    ...mapState("coordinator", ["profile"]),
    ...mapState("user", ["userDetails"]),
  },
}
</script>
