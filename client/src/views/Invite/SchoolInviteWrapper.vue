<template>
  <div class="pa-10">
    <route-tabs :tabs="tabs" introjs="tabs" />
    <v-row>
      <v-col class="mx-auto" sm="11" lg="9">
        <router-view />
      </v-col>
    </v-row>
    <div class="overline text-center">
      *
      {{
        this.$t(
          "invite.invitingUserOrChangingExistingEmailWillSendAnInviteToTheInviteesMailbox"
        )
      }}.
    </div>
  </div>
</template>

<script>
import RouteTabs from "../../components/RouteTabs"
import introjsSubscribeMixin from "../../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "SchoolInviteWrapper",
  components: { RouteTabs },
  mixins: [introjsSubscribeMixin],
  data() {
    return {
      tabs: [
        {
          componentName: "InviteConsumers",
          text: this.$t("invite.inviteStudents"),
        },
        {
          componentName: "InviteCoordinators",
          text: this.$t("invite.inviteStaff"),
        },
      ],
    }
  },
}
</script>
