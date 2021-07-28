<template>
  <actions-table :headers="headers" :items="eventOrders" />
</template>

<script>
import { mapState } from "vuex"
import store from "../vuex/store"
import ActionsTable from "../components/ActionsTable"

export default {
  components: { ActionsTable },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("vendorEvent/getEventOrders")
    next()
  },
  computed: {
    ...mapState("vendorEvent", ["eventOrders"]),
  },
  data() {
    return {
      headers: [
        // { text: this.$t("event."), value: "school_group_name" },
        // { text: this.$t("event."), value: "school_name" },
        // { text: this.$t("event."), value: "activity_name" },
        { text: this.$t("event."), value: "locationsName" },
        { text: this.$t("event."), value: "startTime" },
        { text: this.$t("event."), value: "endTime" },
        { text: this.$t("event."), value: "recurrence" },
        { text: this.$t("event."), value: "status" },
      ],
    }
  },
}
</script>
