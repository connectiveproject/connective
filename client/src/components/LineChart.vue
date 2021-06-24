<script>
import { Line, mixins } from "vue-chartjs"
const { reactiveProp } = mixins

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: {
    options: {
      type: Object,
      default: null,
    },
  },
  mounted() {
    // reactiveProp provides the `chartData` prop, which should be passed from parent
    this.renderChart(this.chartData, this.options)
  },
}
</script>
