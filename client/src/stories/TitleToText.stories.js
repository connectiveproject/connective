import TitleToText from "../components/TitleToText.vue"

//👇 This default export determines where your story goes in the story list
export default {
  title: "TitleToText",
  component: TitleToText,
}

//👇 We create a “template” of how args map to rendering
const Template = args => ({
  components: { TitleToText },
  data() { return { args } },
  template: '<title-to-text v-bind="args" />'
})

export const Primary = Template.bind({})
Primary.args = {
  text: "text",
  title: "title",
}
