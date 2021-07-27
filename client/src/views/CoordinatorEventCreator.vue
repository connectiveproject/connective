<template>
  <v-row class="pa-10">
    <v-col class="mx-auto" sm="11" lg="9">
      <h1 v-text="$t('events.eventsCreation')" />
      <time-input :label="$t(time.startTime)"  />
      <time-input :label="$t(time.endTime)"  />
    </v-col>
  </v-row>

  <!--
    start time
    end time
    day
    school_group
    locations_name
    ocurrence
   -->
</template>

<script>
import TimeInput from "../components/TimeInput"
export default {
  components: { TimeInput },
}
</script>

<style scoped></style>
