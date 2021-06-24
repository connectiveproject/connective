<template>
  <v-card
    class="my-15 mx-auto px-10 py-10"
    max-width="1000"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
  >
    <v-card-title
      class="text-h4"
      v-text="$t('events.unsummarizedPastEvents')"
    />
    <v-card-subtitle
      class="text-h6 pt-3"
      v-text="$t('events.clickAnEventToSummarizeIt')"
    />
    <click-list
      v-if="eventList.length"
      v-model="selected"
      class="my-12"
      :title="$t('events.eventsToSummarize')"
      :items="formattedEvents"
      @input="onEventClick"
    />
  </v-card>
</template>

<script>
import store from "../vuex/store"
import moment from "moment"
import { mapState } from "vuex"
import ClickList from "../components/ClickList"
export default {
  components: { ClickList },
  data() {
    return {
      selected: [],
      isEventClicked: false,
    }
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("instructorEvent/getPastEvents", 60)
    next()
  },
  computed: {
    ...mapState("instructorEvent", ["eventList"]),
    formattedEvents() {
      return this.eventList
        .filter(event => !event.hasSummary)
        .map(event => ({
          action: moment(event.startTime).format("DD.MM.YYYY"),
          subtitle: event.activityName,
          title: event.schoolGroupName,
        }))
    },
  },
  methods: {
    onEventClick(e) {
      // extract event slug & route to event summary
      if (this.isEventClicked) return
      this.isEventClicked = true
      const eventPos = e[0]
      this.$router.push({
        name: "InstructorEventSummary",
        params: { slug: this.eventList[eventPos].slug },
      })
    },
  },
}
</script>
