<template>
  <div>
    <canvas ref="doughnut" />
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
    colors: {
      type: Array,
      default() {
        return []
      },
    },
    data: {
      type: Array,
      default() {
        return []
      },
    },
    options: {
      type: Object,
      default() {
        return Chart.defaults.doughnut
      },
    },
  },
  mounted() {
    this.createChart({
      datasets: [
        {
          data: this.data,
          backgroundColor: this.colors,
        },
      ],
      labels: this.labels,
    })
  },
  methods: {
    createChart(chartData) {
      const canvas = this.$refs.doughnut
      const options = {
        type: "doughnut",
        data: chartData,
        options: this.options,
      }
      new Chart(canvas, options)
    },
  },
}
</script>
