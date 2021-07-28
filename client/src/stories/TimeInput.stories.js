import TimeInput from "../components/TimeInput.vue"

export default {
  title: "TimeInput",
  component: TimeInput,
}

const Template = args => ({
  components: { TimeInput },
  data: () => ({ args }),
  template: `<time-input v-model="args.time" :label="args.label" />`,
})

export const Primary = Template.bind({})
Primary.args = { time: "", label: "choose time" }
