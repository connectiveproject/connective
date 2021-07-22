<template>
  <div>
    <canvas ref="bar" />
  </div>
</template>

<script>
import Chart from "chart.js/auto"

export default {
  props: {
    labels: {
      type: Array,
      default() {
        return []
      },
    },
    datasets: {
      type: Array,
      default() {
        return []
      },
    },
    options: {
      type: Object,
      default() {
        return Chart.defaults.bar
      },
    },
  },
  mounted() {
    this.createChart({
      datasets: this.datasets,
      labels: this.labels,
    })
  },
  methods: {
    createChart(chartData) {
      const canvas = this.$refs.bar
      const options = {
        type: "bar",
        data: chartData,

      }
      new Chart(canvas, options)
    },
  },
}
</script>
