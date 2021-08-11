<template>
  <div>
    <route-tabs :tabs="tabs" introjs="tabs" />
    <router-view />
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
  name: "OrganizationInviteWrapper",
  components: { RouteTabs },
  mixins: [introjsSubscribeMixin],
  data() {
    return {
      tabs: [
        {
          componentName: "InviteInstructors",
          text: this.$t("invite.inviteInstructors"),
        },
        {
          componentName: "InviteVendors",
          text: this.$t("invite.inviteVendors"),
        },
      ],
    }
  },
}
</script>
