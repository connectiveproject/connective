<template>
  <div>
    <h1 v-text="$t('myActivity.myEvents')" class="mb-5" />
    <h2
      v-text="$t('myActivity.hereYouCanSeeAllThePlannedEvents')"
      class="pb-12"
    />
    <v-sheet tile height="70" class="d-flex mx-auto" max-width="500">
      <v-btn icon class="ma-2" @click="$refs.calendar.prev()">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
      <v-select
        v-model="chosenDisplayType"
        :items="displayTypes"
        dense
        outlined
        hide-details
        class="ma-2"
        :label="$t('general.display')"
      />
      <v-btn icon class="ma-2" @click="$refs.calendar.next()">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
    </v-sheet>
    <v-calendar
      v-model="value"
      ref="calendar"
      class="text-center calendar"
      :events="formattedEvents"
      :weekday-format="translateWeekdays"
      :month-format="translateMonths"
      :type="chosenDisplayType"
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
import store from "../vuex/store"
import { mapState, mapActions } from "vuex"
import moment from "moment"
import DetailModal from "../components/DetailModal"
import Utils from "../helpers/utils"

export default {
  components: {
    DetailModal,
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("event/getEventList", {
      benchmarkDate: moment(),
      override: true,
    })
    next()
  },
  methods: {
    ...mapActions("event", ["getEventList"]),
    translateWeekdays(date) {
      // :object date: v-calendar day/date object
      // note: weekday starts from zero
      return this.$t(`time.day-${date.weekday}`)
    },
    translateMonths(date) {
      // :object date: v-calendar day/date object
      // note: month starts from one
      return this.$t(`time.month-${date.month}`)
    },
    showEvent({ event }) {
      this.clickedEvent = event
      this.isModalOpen = true
    },
    fetchEvents(benchmarkDay) {
      // :Object benchmarkDay: the date object to fetch "around" (e.g., )
      const benchmarkDate = moment(benchmarkDay.date)
      this.getEventList({ benchmarkDate, override: true })
    },
  },
  data() {
    return {
      value: null,
      displayTypes: [
        {
          text: this.$t("time.monthly"),
          value: "month",
        },
        {
          text: this.$t("time.weekly"),
          value: "week",
        },
        {
          text: this.$t("time.daily"),
          value: "day",
        },
        {
          text: this.$t("time.halfWeekly"),
          value: "4day",
        },
      ],
      chosenDisplayType: this.$vuetify.breakpoint.mobile ? "4day" : "week",
      clickedEvent: null,
      isModalOpen: false,
    }
  },
  computed: {
    ...mapState("event", ["eventList"]),
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
          color: Utils.getPsuedoRandomColorByString(e.activityName || ""),
          timed: true,
          // Modal related data
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
  line-height: 2;
  padding-bottom: 15px;
}
.calendar::v-deep {
  .v-calendar-daily__head {
    margin-right: 0 !important;
  }
  .v-calendar-daily__scroll-area {
    overflow-y: unset;
  }
  v-event-timed-container {
    margin-right: 0px;
    margin-left: 10px;
  }
}
</style>
