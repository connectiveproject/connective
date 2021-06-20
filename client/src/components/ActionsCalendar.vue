<template>
  <div>
    <v-sheet tile height="70" class="d-flex mx-auto" max-width="500">
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
        :label="$t('general.display')"
      />
      <v-btn icon class="ma-2" @click="$refs.calendar.next()">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
    </v-sheet>
    <calendar
      :type="displayType"
      ref="calendar"
      v-bind="$attrs"
      v-on="$listeners"
    />
  </div>
</template>

<script>
import Calendar from "./Calendar.vue"
export default {
  components: { Calendar },
  inheritAttrs: false,
  props: {
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
