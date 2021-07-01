import { action } from "@storybook/addon-actions"
import StickyNote from "../components/StickyNote.vue"

export default {
  title: "StickyNote",
  component: StickyNote,
}

const Template = args => ({
  components: { StickyNote },
  methods: { action },
  data: () => ({ args }),
  template: `
    <sticky-note>
     {{ args.defaultSlot }}
    </sticky-note>
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  defaultSlot: "My name is Sticky Bob, what's yours",
}
