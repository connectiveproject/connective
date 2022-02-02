<template>
  <div>
    <h1 class="pb-4" v-text="$t('events.eventsSummary')" />
    <h2
      v-text="$t('events.hereYouCanViewAllThePastEventsAndTheirAttendance')"
      class="pb-12"
    />
    <base-pagination-table
      introjs="events-table"
      class="mb-10"
      :loading="loading"
      :headers="headers"
      :items="readablePastEvents"
      @paginate="getEvents"
    >
      <template slot="footer.prepend">
        <v-btn
          class="px-5"
          color="primary"
          @click="exportEvents"
          v-text="$t('userActions.export')"
        />
      </template>
    </base-pagination-table>
  </div>
</template>
<script>
import { mapState, mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "@/vuex/store"
import Utils from "@/helpers/utils"
import { SERVER } from "@/helpers/constants/constants"
import BasePaginationTable from "@/components/Tables/BasePaginationTable"
import introjsSubscribeMixin from "@/mixins/introJs/introjsSubscribeMixin"

export default {
  name: "EventSummaryList",
  components: { BasePaginationTable },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("vxEventList/getPastEvents", {
      override: true,
      usePagination: true,
    })
    next()
  },
  computed: {
    ...mapState("vxEventList", ["pastEvents"]),
    readablePastEvents() {
      return this.pastEvents.map(e => ({
        ...e,
        isCanceled: e.isCanceled
          ? this.$t("general.yes")
          : this.$t("general.no"),
        cancellationReason: e.cancellationReason
          ? this.$t(
              `eventCancellationReasons.${Utils.getKeyByValue(
                SERVER.eventCancellationReasons,
                e.cancellationReason
              )}`
              // eslint-disable-next-line indent
            )
          : "",
        hasSummary: e.hasSummary
          ? this.$t("general.yes")
          : this.$t("general.no"),
        startTime: Utils.ApiStringToReadableDate(e.startTime),
        endTime: Utils.ApiStringToReadableDate(e.endTime),
      }))
    },
  },
  data() {
    return {
      loading: false,
      headers: [
        {
          text: this.$t("groups.groupName"),
          value: "schoolGroupName",
          sortable: false,
        },
        {
          text: this.$t("program.programName"),
          value: "activityName",
          sortable: false,
        },
        { text: this.$t("events.eventSummarized"), value: "hasSummary" },
        { text: this.$t("general.isCancelled"), value: "isCanceled" },
        {
          text: this.$t("general.cancellationReason"),
          value: "cancellationReason",
        },
        {
          text: this.$t("events.registeredCount"),
          value: "totalConsumersCount",
          sortable: false,
        },
        {
          text: this.$t("events.attendantsCountAccordingToSummary"),
          value: "attendedConsumersCount",
          sortable: false,
        },
        {
          text: this.$t("general.instructor"),
          value: "instructorName",
          sortable: false,
        },
        { text: this.$t("time.startDate"), value: "startTime" },
        { text: this.$t("time.endDate"), value: "endTime" },
      ],
    }
  },
  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("vxEventList", ["getPastEvents", "getPastEventsExportFile"]),
    async getEvents() {
      this.loading = true
      await this.getPastEvents({ override: true, usePagination: true })
      this.loading = false
    },
    exportEvents: debounce(
      function () {
        return this.getPastEventsExportFile({ usePagination: true })
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
