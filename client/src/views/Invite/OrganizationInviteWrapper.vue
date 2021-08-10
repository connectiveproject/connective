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
import introjsMixin from "../../mixins/introJs/introjsMixin"

export default {
  components: { RouteTabs },
  mixins: [introjsMixin],
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
