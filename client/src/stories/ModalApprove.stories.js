import { action } from "@storybook/addon-actions"
import ModalApprove from "../components/ModalApprove.vue"

export default {
  title: "ModalApprove",
  component: ModalApprove,
}

const Template = args => ({
  components: { ModalApprove },
  methods: { action },
  data: () => ({ args }),
  template: `
    <modal-approve
      v-model="args.isOpen"
      @input="action('input')()"
      @approve="action('approve')()"
      @disapprove="action('disapprove')()"
    >
      {{ args.defaultSlot }}
    </modal-approve>
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  isOpen: true,
  defaultSlot: "האם אתם בטוחים שברצונכם למחוק?",
}
