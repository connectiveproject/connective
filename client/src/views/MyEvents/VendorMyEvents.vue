<template>
  <div class="ma-3 pa-3 px-lg-16 mx-lg-16 py-lg-6 my-lg-6">
    <div class="d-flex flex-wrap mb-10 justify-space-between">
      <div>
        <h1 v-text="$t('events.eventsCalendar')" />
        <h2
          v-text="$t('myActivity.hereYouCanSeeAllThePlannedEvents')"
          class="pb-10"
        />
      </div>
    </div>
    <actions-calendar
      v-model="value"
      introjs="events-calendar"
      first-interval="5"
      interval-count="19"
      :displayType.sync="chosenDisplayType"
      :events="formattedEvents"
      @click:event="showEvent"
      @moved="fetchEvents"
    />
    <event-edit-dialog
      v-if="clickedEvent"
      :event="clickedEvent.eventObject"
      :group="clickedEventGroup"
      @eventUpdated="eventUpdated"
      v-model="isModalOpen"
      @close="clickedEvent = null"
    />
  </div>
</template>

<script>
import store from "@/vuex/store"
import { mapState, mapActions } from "vuex"
import moment from "moment"
import Api from "@/api"
import ActionsCalendar from "@/components/ActionsCalendar"
import EventEditDialog from "@/components/EventEditDialog"
import Utils from "@/helpers/utils"
import introjsSubscribeMixin from "@/mixins/introJs/introjsSubscribeMixin"

export default {
  name: "MyEvents",
  components: {
    ActionsCalendar,
    EventEditDialog,
  },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 700 })
    await store.dispatch("vendorEvent/getEventList", {
      benchmarkDate: moment(),
      override: true,
      usePagination: true,
    })
    next()
  },
  methods: {
    // TODO: change to relevant action
    ...mapActions("vendorEvent", ["getEventList"]),
    async showEvent({ event }) {
      const group = await Api.programGroup.getGroup(
        event.eventObject.schoolGroup
      )
      this.clickedEvent = event
      this.clickedEventGroup = group["data"]
      this.isModalOpen = true
    },
    fetchEvents(benchmarkDay) {
      // :Object benchmarkDay: the date object to fetch "around" (e.g., )
      const benchmarkDate = moment(benchmarkDay.date)
      this.getEventList({ benchmarkDate, override: true, usePagination: true })
    },
    async eventUpdated(benchmarkDay) {
      // called by the EventEditDialog after save - we need to refresh
      this.fetchEvents(benchmarkDay)
    },
  },
  data() {
    return {
      value: "",
      chosenDisplayType: this.$vuetify.breakpoint.xs ? "4day" : "week",
      clickedEvent: null,
      clickedEventGroup: null,
      isModalOpen: false,
    }
  },
  computed: {
    ...mapState("vendorEvent", ["eventList"]),
    formattedEvents() {
      // TODO: consider removal of most of the data (replaced by EDIT) - on original file as well
      return this.eventList.map(e => {
        const start = moment(e.startTime)
        const end = moment(e.endTime)
        const startStr = start.format("DD/MM/YYYY HH:mm")
        const endStr = end.format("DD/MM/YYYY HH:mm")

        return {
          start: start.toDate(),
          end: end.toDate(),
          name: e.activityName || this.$t("errors.nameUnavailable"),
          color: Utils.stringToPsuedoRandomColor(e.activityName || ""),
          timed: true,
          // attaching also Modal related data for onClick usage:
          title: e.activityName,
          bottomSubtitle: e.schoolGroupName,
          body: `
           1. ${this.$t("myActivity.location")}: ${
            e.locationsName || this.$t("errors.empty")
          }
           2. ${this.$t("time.startTime")}: ${startStr}
           3. ${this.$t("time.endTime")}: ${endStr}
           `,
          eventObject: e, // the original event object
        }
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.modalBody {
  white-space: pre-line;
  line-height: 2.3;
  padding-bottom: 5px;
  margin-top: -20px;
}
</style>
