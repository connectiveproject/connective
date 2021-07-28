<template>
  <actions-table
    :headers="headers"
    :items="eventOrders"
    @action-one-click="approveOrder"
    @action-two-click="denyOrder"
  />
</template>

<script>
import { mapState, mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Api from "../api"
import { SERVER } from "../helpers/constants/constants"
import ActionsTable from "../components/ActionsTable"

export default {
  components: { ActionsTable },
  async beforeRouteEnter(to, from, next) {
    console.log(await store.dispatch("vendorEvent/getEventOrders"))
    next()
  },
  computed: {
    ...mapState("vendorEvent", ["eventOrders"]),
  },
  data() {
    return {
      headers: [
        { text: this.$t("groups.groupName"), value: "schoolGroupName" },
        { text: this.$t("general.schoolName"), value: "schoolName" },
        { text: this.$t("program.programName"), value: "activityName" },
        { text: this.$t("myActivity.location"), value: "locationsName" },
        { text: this.$t("time.startTime"), value: "startTime" },
        { text: this.$t("time.endTime"), value: "endTime" },
        { text: this.$t("time.recurrence"), value: "recurrence" },
        { text: this.$t("general.status"), value: "status" },
      ],
    }
  },
  methods: {
    ...mapActions("vendorEvent", ["updateEventOrder"]),
    ...mapActions("snackbar", ["showMessage"]),
    approveOrder: debounce(
      async function (order) {
        ////// console.log(Add approve modal!)
        try {
          await this.updateEventOrder({
            slug: order.slug,
            data: { status: SERVER.eventOrderStatus.approved },
          })
          this.showMessage(this.$t("success.eventSuccessfullyApproved"))
        } catch (err) {
          this.showMessage(Api.utils.parseResponseError(err))
        }
      },
      500,
      { leading: true, trailing: false }
    ),
    denyOrder: debounce(
      async function (order) {
        ////// Add approve modal with rejection text!
        try {
          await this.updateEventOrder({
            slug: order.slug,
            data: { status: SERVER.eventOrderStatus.denied },
          })
          this.showMessage(this.$t("success.eventDenied"))
        } catch (err) {
          console.log(err)
          this.showMessage(Api.utils.parseResponseError(err))
        }
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
