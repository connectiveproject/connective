import { action } from "@storybook/addon-actions"
import HoverButton from "../components/HoverButton.vue"

export default {
  title: "HoverButton",
  component: HoverButton,
}

const Template = args => ({
  components: { HoverButton },
  methods: { action },
  data: () => ({ args }),
  template: `
    <hover-button
    @click="action('click')()"
    class="mx-auto"
    circle
    >
      <!-- default slot: -->
      <img style="border-radius: 50%" src="https://picsum.photos/200">
    </hover-button>
    `,
})

export const Primary = Template.bind({})
Primary.args = {}
