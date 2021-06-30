<template>
  <div>
    <h1 v-text="$t('myActivity.statistics')" class="mb-5" />
    <h2
      v-text="$t('myActivity.advancedViewOfAllYourActivities')"
      class="pb-12"
    />
    <bubble-chart
      class="mx-auto"
      :data="bubbleChartData"
      :label="bubbleChartLabel"
    />
    <doughnut
      style="width: 450px;"
      class="mx-auto my-10"
      :data="doughnutChartData"
      :labels="doughnutChartLabels"
    />
  </div>
</template>

<script>
import { mapState } from "vuex"
import store from "../vuex/store"
import BubbleChart from "../components/Charts/BubbleChart"
import Doughnut from "../components/Charts/Doughnut"
export default {
  components: { BubbleChart, Doughnut },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("program/getTopConsumerRequestsStats")
    next()
  },
  data() {
    return {
      bubbleChartLabel: this.$t(
        "myActivity.mostPopularProgramsByPendingRequests"
      ),
    }
  },
  computed: {
    ...mapState("program", ["topConsumerRequestsStats"]),
    bubbleChartData() {
      return this.topConsumerRequestsStats.map(program => ({
        x: Math.random() * 30,
        y: Math.random() * 30,
        r: program.consumerRequests * 10,
        label: `${program.activityName} (${program.consumerRequests})`,
      }))
    },
    doughnutChartLabels() {
      return this.topConsumerRequestsStats.map(program => program.activityName)
    },
    doughnutChartData() {
      return this.topConsumerRequestsStats.map(program => program.consumerRequests)
    },
  },
}
</script>
