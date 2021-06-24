<template>
  <v-card>
    <v-card-title v-text="event.schoolGroupName" />
    <v-card-title v-text="event.activityName" />
    <title-to-text :title="$t('time.startTime')" :text="startTime" />
    <title-to-text :title="$t('time.endTime')" :text="endTime" />
    <title-to-text
      :title="$t('myActivity.location')"
      :text="locations_name || $t('errors.empty')"
    />

    <hr />

    <!-- input drawer -->
    <!--
            "activity_name": "מגשימים",
            "school_group_name": "מגשימים א' רימונים",
            "start_time": "2021-06-15T08:00:00+03:00",
            "end_time": "2021-06-15T10:00:00+03:00",
            "consumers": [
                2
            ],
            "school_group": 3,
            "locations_name": null,
            "has_summary": false,
            "summary_general_notes": null,
            "summary_general_rating": null,
            "summary_children_behavior": null
 -->
  </v-card>
</template>

<script>
import TitleToText from "../components/TitleToText"
import store from "../vuex/store"

export default {
  components: { TitleToText },
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  async beforeRouteEnter(to, from, next) {
    const event = await store.dispatch(
      "instructorEvent/getEvent",
      to.params.slug
    )
    next(vm => (vm.event = event))
  },
  data() {
    return {
      event: null,
    }
  },
}
</script>
