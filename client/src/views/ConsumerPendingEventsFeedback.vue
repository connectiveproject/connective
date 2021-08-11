<template>
  <v-card
    class="mx-3 my-15 mx-md-auto px-sm-10 py-sm-10"
    max-width="1000"
    :min-height="$vuetify.breakpoint.mobile ? 350 : 500"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
  >
    <v-card-title class="text-sm-h4" v-text="$t('events.eventsFeedback')" />
    <v-card-subtitle
      class="text-md-h6 pt-3"
      v-text="$t('events.clickAnEventToGiveFeedbackSoWeCanImproveTogether!')"
    />
    <click-list
      introjs="click-list"
      v-if="formattedEvents.length"
      v-model="selected"
      class="my-12"
      :title="$t('events.eventsToSummarize')"
      :items="formattedEvents"
      @input="onEventClick"
    />
    <div
      v-else
      class="text-center text-md-h6 absolute-center text-body-1"
      v-text="$t('events.eventsToFeedbackWereNotFound')"
    />
  </v-card>
</template>

<script>
import store from "../vuex/store"
import moment from "moment"
import ClickList from "../components/ClickList"
import introjsSubscribeMixin from "../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "ConsumerPendingEventsFeedback",
  components: { ClickList },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    const events = await store.dispatch("consumerEvent/getPastEvents", 60)
    next(vm => (vm.eventsToFeedback = events.filter(e => !e.hasFeedback)))
  },
  data() {
    return {
      selected: [],
      isEventClicked: false,
      eventsToFeedback: null,
    }
  },
  computed: {
    formattedEvents() {
      if (!this.eventsToFeedback) return []
      return this.eventsToFeedback.map(event => ({
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
        name: "ConsumerEventFeedback",
        params: { slug: this.eventsToFeedback[eventPos].slug },
      })
    },
  },
}
</script>
