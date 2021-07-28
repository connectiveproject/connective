import DateInput from "../components/DateInput.vue"

export default {
  title: "DateInput",
  component: DateInput,
}

const Template = args => ({
  components: { DateInput },
  data: () => ({ args }),
  template: `<date-input v-model="args.date" :label="label" />`,
})

export const Primary = Template.bind({})
Primary.args = {
  date: "",
  label: "choose date!",
}
