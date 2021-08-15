<template>
  <div class="ma-3 pa-3 px-lg-16 mx-lg-16 py-lg-6 my-lg-6">
    <h1 v-text="$t('events.eventsBoard')" class="mb-5" />
    <h2
      v-text="$t('myActivity.hereYouCanSeeAllThePlannedEvents')"
      class="pb-12"
    />
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
    <detail-modal
      v-if="clickedEvent"
      v-model="isModalOpen"
      :title="clickedEvent.title || ''"
      :topSubtitle="$t('myActivity.eventDetails')"
      :bottomSubtitle="clickedEvent.bottomSubtitle || ''"
      :buttonText="$t('userActions.close')"
    >
      <div class="modalBody">
        {{ clickedEvent.body }}
      </div>
    </detail-modal>
  </div>
</template>

<script>
import store from "../../vuex/store"
import { mapState, mapActions } from "vuex"
import moment from "moment"
import ActionsCalendar from "../../components/ActionsCalendar"
import DetailModal from "../../components/DetailModal"
import Utils from "../../helpers/utils"
import introjsSubscribeMixin from "../../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "ConsumerMyEvents",
  components: {
    DetailModal,
    ActionsCalendar,
  },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("consumerEvent/getEventList", {
      benchmarkDate: moment(),
      override: true,
      usePagination: false,
    })
    next()
  },
  methods: {
    ...mapActions("consumerEvent", ["getEventList"]),
    showEvent({ event }) {
      this.clickedEvent = event
      this.isModalOpen = true
    },
    fetchEvents(benchmarkDay) {
      // :Object benchmarkDay: the date object to fetch "around" (e.g., )
      const benchmarkDate = moment(benchmarkDay.date)
      this.getEventList({ benchmarkDate, override: true, usePagination: false })
    },
  },
  data() {
    return {
      value: "",
      chosenDisplayType: this.$vuetify.breakpoint.xs ? "4day" : "week",
      clickedEvent: null,
      isModalOpen: false,
    }
  },
  computed: {
    ...mapState("consumerEvent", ["eventList"]),
    formattedEvents() {
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
