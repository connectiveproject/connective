<template>
  <div>
    <canvas class="bubble" ref="bubble" />
  </div>
</template>

<script>
import Chart from "chart.js/auto"
import ChartDataLabels from "chartjs-plugin-datalabels"

export default {
  props: {
    label: {
      type: String,
      default: "",
    },
    color: {
      type: String,
      default: "#4BC0C0",
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
        return {}
      },
    },
  },
  mounted() {
    this.createChart({
      datasets: [
        {
          label: this.label,
          data: this.data,
          backgroundColor: this.color,
          datalabels: {
            formatter(value) {
              return value.label
            },
          },
        },
      ],
    })
  },
  methods: {
    createChart(chartData) {
      const canvas = this.$refs.bubble
      const options = {
        type: "bubble",
        data: chartData,
        options: this.opts,
        plugins: [ChartDataLabels],
      }
      new Chart(canvas, options)
    },
  },
  computed: {
    opts() {
      return Object.assign(
        {
          scales: {
            x: {
              ticks: {
                callback() {
                  return ""
                },
              },
            },
            y: {
              ticks: {
                callback() {
                  return ""
                },
              },
            },
          },
          plugins: {
            datalabels: {
              align: "start",
              anchor: "start",
              textAlign: "center",
            },

            tooltip: {
              callbacks: {
                label(context) {
                  return context.raw.label
                },
              },
              rtl: true,
            },
          },
        },
        this.options
      )
    },
  },
}
</script>
