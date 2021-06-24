import { action } from "@storybook/addon-captions"
import ClickList from "../components/ClickList"

export default {
  title: "ClickList",
  component: ClickList,
}

const Template = args => ({
  components: { ClickList },
  methods: { action },
  data: () => ({ args }),
  template: `
    <click-list
    class="mx-auto"
    v-model="args.selected"
    :items="args.items"
    :title="args.title"
    @input="action('input')()"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  selected: [],
  title: "Title",
  items: [
    {
      caption: "15 min",
      headline: "Brunch this weekend?",
      subtitle: `I'll be in your neighborhood doing errands this weekend. Do you want to hang out?`,
      title: "Ali Connors",
    },
    {
      caption: "2 hr",
      headline: "Summer BBQ",
      subtitle: `Wish I could come, but I'm out of town this weekend.`,
      title: "me, Scrott, Jennifer",
    },
    {
      caption: "6 hr",
      headline: "Oui oui",
      subtitle: "Do you have Paris recommendations? Have you ever been?",
      title: "Sandra Adams",
    },
    {
      caption: "12 hr",
      headline: "Birthday gift",
      subtitle:
        "Have any ideas about what we should get Heidi for her birthday?",
      title: "Trevor Hansen",
    },
    {
      caption: "18hr",
      headline: "Recipe to try",
      subtitle:
        "We should eat this: Grate, Squash, Corn, and tomatillo Tacos.",
      title: "Britta Holt",
    },
  ],
}
