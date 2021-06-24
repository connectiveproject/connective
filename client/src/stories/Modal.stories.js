import { action } from "@storybook/addon-actions"
import Modal from "../components/Modal.vue"

export default {
  title: "Modal",
  component: Modal,
}

const Template = args => ({
  components: { Modal },
  methods: { action },
  data: () => ({ args }),
  template: `
    <modal
    class="mx-auto"
    v-model="args.modalOptions"
    @close="action('close')()"
    >
    <template v-slot:header>
      {{ args.headerSlot }}
    </template>

    {{ args.defaultSlot }}

    <template v-slot:btn>
      {{ args.btnSlot }}
    </template>

    </modal>
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  defaultSlot: "default slot",
  headerSlot: "Title",
  btnSlot: "Click Me",
}
