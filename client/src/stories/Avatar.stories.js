import { action } from "@storybook/addon-actions"
import Avatar from "../components/Avatar/Avatar.vue"

export default {
  title: "Avatar",
  component: Avatar,
}

const Template = args => ({
  components: { Avatar },
  methods: { action },
  data: () => ({ args }),
  template: `
    <avatar
    style="width: 200px;"
    class="mx-auto"
    v-model="args.avatarOptions"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  // avatarOptions: {
  //   clotheType: "GraphicShirt",
  //   eyebrowType: "Angry",
  //   eyeType: "Cry",
  //   mouthType: "Eating",
  //   facialHairColor: "Blonde",
  //   graphicType: "Cumbia",
  // },
  avatarOptions: {},
}
