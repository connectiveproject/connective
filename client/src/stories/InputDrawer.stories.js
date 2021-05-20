import InputDrawer from "../components/InputDrawer.vue"

//👇 This default export determines where your story goes in the story list
export default {
  title: "InputDrawer",
  component: InputDrawer,
}

//👇 We create a “template” of how args map to rendering
const Template = args => ({
  components: { InputDrawer },
  data() { return { args } },
  template: '<InputDrawer v-bind="args" />'
})

export const Primary = Template.bind({})
Primary.args = {
  text: "text",
  title: "title",
}
