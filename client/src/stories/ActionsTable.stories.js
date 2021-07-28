import { action } from "@storybook/addon-actions"
import ActionsTable from "../components/ActionsTable"

export default {
  title: "ActionsTable",
  component: ActionsTable,
}

const Template = args => ({
  components: { ActionsTable },
  methods: { action },
  data: () => ({ args }),
  template: `
    <actions-table
      class="w-75 mx-auto"
      v-bind="args"
      @action-one-click="action('action-one-click')()"
      @action-two-click="action('action-two-click')()"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  headers: [
    { text: "Food Name", value: "name" },
    { text: "Num of Cals", value: "calories" },
  ],
  items: [
    {
      name: "Banana",
      calories: "70",
    },
    {
      name: "Orange",
      calories: "40",
    },
    {
      name: "Cucumber",
      calories: "35",
    },
    {
      name: "Lemon",
      calories: "45",
    },
    {
      name: "Carrot",
      calories: "20",
    },
    {
      name: "Cookie",
      calories: "45",
    },
    {
      name: "Cake",
      calories: "100",
    },
    {
      name: "Burger",
      calories: "200",
    },
    {
      name: "French Fries",
      calories: "100",
    },
    {
      name: "Water",
      calories: "0",
    },
  ],
}
