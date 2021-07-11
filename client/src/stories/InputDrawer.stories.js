import { action } from "@storybook/addon-actions"
import InputDrawer from "../components/InputDrawer.vue"

export default {
  title: "InputDrawer",
  component: InputDrawer,
  argTypes: { type: { action: "input" } },
}

const Template = args => ({
  components: { InputDrawer },
  methods: { action },
  data: () => ({ args }),
  template: `
  <input-drawer
  style="margin: 0 80px;"
  v-model="args.value"
  v-bind="args"
  @input="action('input')()" />`
})

export const TextInput = Template.bind({})
TextInput.args = {
  uniqueName: "firstName",
  label: "שם פרטי",
  rules: "required",
  value: "בנג'מין",
}

export const SelectInput = Template.bind({})
SelectInput.args = {
  type: "select",
  uniqueName: "Options",
  label: "אפשרויות",
  rules: "required",
  value: [],
  choices: [
    { value: 1, text: "Option A" },
    { value: 2, text: "Option B" },
    { value: 3, text: "Option C" },
  ],
}
