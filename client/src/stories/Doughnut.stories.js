import { action } from "@storybook/addon-actions"
import Doughnut from "../components/Charts/Doughnut.vue"

export default {
  title: "Doughnut",
  component: Doughnut,
}

const Template = args => ({
  components: { Doughnut },
  methods: { action },
  data: () => ({ args }),
  template: `
    <doughnut
    style="width: 500px;"
    class="mx-auto"
    :data="args.data"
    :labels="args.labels"
    :colors="args.colors"
    />
  `,
})

export const Primary = Template.bind({})
Primary.args = {
  colors: ["#FFAEBC", "#A0E7E5", "#B4F8C8", "#FBE7C6"],
  labels: ["A", "B", "C", "D"],
  data: [25, 75, 30, 15],
}
