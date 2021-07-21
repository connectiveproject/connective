import { action } from "@storybook/addon-actions"
import EditableAvatar from "../components/Avatar/EditableAvatar"

export default {
  title: "EditableAvatar",
  component: EditableAvatar,
}

const Template = args => ({
  components: { EditableAvatar },
  methods: { action },
  data: () => ({ args }),
  template: `
    <editable-avatar
    style="width: 200px;"
    class="mx-auto"
    v-model="args.avatarOptions"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  avatarOptions: {},
}
