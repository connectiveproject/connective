<template>
  <div class="pa-3 pa-sm-10">
    <route-tabs :tabs="visibleTabs" introjs="tabs" />
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
import Utils from "@/helpers/utils"

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
          privileges: ["PRIV_USER_CONSUMER_EDIT"],
        },
        {
          componentName: "InviteCoordinators",
          text: this.$t("invite.inviteStaff"),
          privileges: ["PRIV_USER_COORDINATOR_EDIT"],
        },
      ],
    }
  },
  computed: {
    visibleTabs() {
      return this.tabs.filter(tab => tab.privileges.some(Utils.hasPrivilege))
    },
  },
}
</script>
