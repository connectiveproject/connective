import { action } from "@storybook/addon-actions"
import SelectTable from "../components/SelectTable"

export default {
  title: "SelectTable",
  component: SelectTable,
}

const Template = args => ({
  components: { SelectTable },
  methods: { action },
  data: () => ({ args }),
  template: `
    <select-table
      class="w-75 mx-auto"
      v-bind="args"
      v-model="args.selected"
      @input="action('input')()"
      @select="action('select')()"
      @diselect="action('diselect')()"
      >
    </select-table>

    `,
})

export const Primary = Template.bind({})
Primary.args = {
  headers: [
    { text: "Food Name", value: "name" },
    { text: "Num of Cals", value: "calories" },
  ],
  selected: [
    {
      name: "Banana",
      calories: "70",
    },
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
