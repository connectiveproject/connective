import { action } from "@storybook/addon-actions"
import BubbleChart from "../components/Charts/BubbleChart.vue"

export default {
  title: "BubbleChart",
  component: BubbleChart,
}

const Template = args => ({
  components: { BubbleChart },
  methods: { action },
  data: () => ({ args }),
  template: `
    <bubble-chart
    style="width: 500px;"
    class="mx-auto"
    :data="args.data"
    :label="args.label"
    :color="args.color"
    />
  `,
})

export const Primary = Template.bind({})
Primary.args = {
  color: "#FFAEBC",
  data: [
    {
      x: 5,
      y: 5,
      r: 15,
      label: "label2"
    },
    {
      x: 10,
      y: 10,
      r: 30,
      label: "label1",
    },
  ],
}
