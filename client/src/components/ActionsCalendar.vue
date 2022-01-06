<template>
  <div>
    <v-sheet
      tile
      class="d-flex relative mx-auto py-6 align-center justify-center flex-wrap"
    >
      <div class="d-flex flex-wrap align-center justify-center actions">
        <v-btn icon class="ma-2" @click="$refs.calendar.prev()">
          <v-icon :class="{ mirror: checkRtl() }">mdi-chevron-left</v-icon>
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
          <v-icon :class="{ mirror: checkRtl() }">mdi-chevron-right</v-icon>
        </v-btn>
        <v-btn
          color="primary"
          class="my-2 mx-5"
          :class="{ action: $vuetify.breakpoint.xs }"
          @click="setToday"
          v-text="$t('time.today')"
        />
      </div>
      <div
        :class="{ 'absolute-left': $vuetify.breakpoint.mdAndUp }"
        class="text--center text-h5 font-weight-bold"
        v-text="title"
      />
    </v-sheet>
    <calendar
      ref="calendar"
      v-bind="$attrs"
      v-on="$listeners"
      :type="displayType"
      :value="value"
      @input="$emit('input', $event)"
      @change="setTitle"
    />
  </div>
</template>

<script>
import Utils from "@/helpers/utils"
import Calendar from "@/components/Calendar"

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
    checkRtl: Utils.checkRtl,
    setTitle() {
      this.title = this.$refs.calendar.$refs.calendar.title
    },
    onDisplayTypeChange(e) {
      this.$emit("update:displayType", e)
    },
    async setToday() {
      this.$emit("input", "")
      await this.$nextTick()
      // emit calendar's `moved` event
      this.$refs.calendar.move(0)
    }
  },
  data() {
    return {
      title: "",
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
.actions {
  max-width: 500px;
}
</style>
