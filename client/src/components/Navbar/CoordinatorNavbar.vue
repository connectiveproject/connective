<template>
  <v-toolbar dark prominent :src="bg">
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
    <template v-slot:extension>
      <route-tabs :tabs="buttons" color="primary" class="px-md-6" />
    </template>
  </v-toolbar>
</template>

<script>
import { mapState } from "vuex"
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
