import ChipContainer from "../components/ChipContainer.vue"

export default {
  title: "ChipContainer",
  component: ChipContainer,
}

const Template = args => ({
  components: { ChipContainer },
  data() {
    return { args }
  },
  template: `
  <chip-container
    style="width: 400px; padding: 20px;"
    v-bind="args"
  >
    {{ args.defaultSlot }}
  </chip-container>
  `,
})

export const Primary = Template.bind({})
Primary.args = {
  labels: ['David', 'Albert', 'Rachel', 'Amy', 'Benny'],
  icon: "mdi-account-circle",
  defaultSlot: "Title"
}
