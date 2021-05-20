import InputDrawer from "../components/InputDrawer.vue"

//👇 This default export determines where your story goes in the story list
export default {
  title: "InputDrawer",
  component: InputDrawer,
}

//👇 We create a “template” of how args map to rendering
const Template = args => ({
  components: { InputDrawer },
  data() {
    return { args }
  },
  template: `<InputDrawer v-model="args.value" v-bind="args" />`,
})

export const TextInput = Template.bind({})
TextInput.args = {
  inputType: "text",
  uniqueName: "firstName",
  descriptiveName: "שם פרטי",
  validationRules: "required",
  value: "בנג'מין",
}

export const SelectInput = Template.bind({})
SelectInput.args = {
  inputType: "select",
  uniqueName: "Options",
  descriptiveName: "אפשרויות",
  validationRules: "required",
  value: [],
  selectItems: [
    { value: 1, text: "Option A" },
    { value: 2, text: "Option B" },
    { value: 3, text: "Option C" },
  ],
}
