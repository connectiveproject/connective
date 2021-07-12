<template>
  <div>
    <route-tabs :tabs="tabs" />
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

export default {
  components: { RouteTabs },
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
