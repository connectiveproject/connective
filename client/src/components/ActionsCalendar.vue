<template>
  <div>
    <v-sheet tile class="d-flex mx-auto py-6" max-width="500">
      <div class="d-flex flex-wrap justify-center">
        <v-btn icon class="ma-2" @click="$refs.calendar.prev()">
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
        <v-select
          value="displayType"
          @input="onDisplayTypeChange"
          :items="displayTypes"
          dense
          outlined
          hide-details
          class="ma-2"
          :class="{ action: $vuetify.breakpoint.xs }"
          :label="$t('general.display')"
        />
        <v-btn icon class="ma-2" @click="$refs.calendar.next()">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <v-btn
          color="primary"
          class="ma-2"
          :class="{ action: $vuetify.breakpoint.xs }"
          @click="e => $emit('input', '')"
          v-text="$t('time.today')"
        />
      </div>
    </v-sheet>
    <calendar
      ref="calendar"
      v-bind="$attrs"
      v-on="$listeners"
      :type="displayType"
      :value="value"
      @input="e => $emit('input', e)"
    />
  </div>
</template>

<script>
import Calendar from "./Calendar.vue"
export default {
  components: { Calendar },
  inheritAttrs: false,
  props: {
    value: {
      // pass empty string for current date
      required: true,
      type: [String, Number, Date],
    },
    displayType: {
      type: String,
      required: true,
      validator(value) {
        return ["month", "week", "day", "4day"].includes(value)
      },
    },
  },
  methods: {
    onDisplayTypeChange(e) {
      this.$emit("update:displayType", e)
    },
  },
  data() {
    return {
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
    }
  },
}
</script>
<style scoped>
.action {
  width: 150px;
}
</style>
