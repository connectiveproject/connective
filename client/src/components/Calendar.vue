<template>
  <v-calendar
    ref="calendar"
    class="text-center"
    v-bind="$attrs"
    v-on="$listeners"
    :weekday-format="translateWeekdays"
    :month-format="translateMonths"
    :value="value"
    @input="$emit('input', $event)"
    @change="$emit('titleChange', $event)"
  />
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    value: {
      required: true,
      type: [String, Number, Date],
    },
  },
  methods: {
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

    // v-calendar methods go here:
    prev(amount = 1) {
      return this.$refs.calendar.prev(amount)
    },
    next(amount = 1) {
      return this.$refs.calendar.next(amount)
    },
    move(amount = 1) {
      return this.$refs.calendar.move(amount)
    },
  },
}
</script>

<style lang="scss" scoped>
.rtl::v-deep {
  .v-calendar-daily__head {
    margin-right: 0 !important;
    .v-calendar-daily_head-day .v-calendar-daily_head-day-label button {
      margin-right: -14px;
      margin-left: -14px;
    }
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
