import { action } from "@storybook/addon-actions"
import TableRowsToChips from "../components/TableRowsToChips"

export default {
  title: "TableRowsToChips",
  component: TableRowsToChips,
}

const Template = args => ({
  components: { TableRowsToChips },
  methods: { action },
  data: () => ({ args }),
  template: `
    <table-rows-to-chips
      class="w-75 mx-auto"
      v-model="args.selected"
      :items="args.items"
      :headers="args.headers"
      :chips-label-header="args.chipsLabelHeader"
      @input="action('input')()"
      >
    </table-rows-to-chips>

    `,
})

export const Primary = Template.bind({})
Primary.args = {
  chipsLabelHeader: "name",
  selected: [
    {
      name: "Banana",
      calories: "70",
    },
  ],
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
