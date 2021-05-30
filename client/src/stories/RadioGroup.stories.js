import { action } from "@storybook/addon-actions"
import RadioGroup from "../components/RadioGroup.vue"

export default {
  title: "RadioGroup",
  component: RadioGroup,
}

const Template = args => ({
  components: { RadioGroup },
  methods: { action },
  data: () => ({ args }),
  template: `
    <radio-group
    class="mx-auto"
    style="width: 800px;"
    v-model="args.selectedItem"
    :title="args.title"
    :choices="args.choices"
    @input="action('input')()"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  title: "בחרו את הפוקימון האהוב עליכם",
  selectedItem: "",
  choices: [
    {
      label: "פיקאצ'ו",
      value: "pikachu",
    },
    {
      label: "צ'אריזרד",
      value: "charizard",
    },
    {
      label: "בולבזאור",
      value: "bulbasaur",
    },
    {
      label: "סנורלאקס",
      value: "snorlax",
    },
  ],
}
