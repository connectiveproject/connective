import { action } from "@storybook/addon-actions"
import FormDialog from "../components/FormDialog.vue"

export default {
  title: "FormDialog",
  component: FormDialog,
}

const Template = args => ({
  components: { FormDialog },
  methods: { action },
  data: () => ({ args }),
  template: `
    <form-dialog
    class="mx-auto"
    style="width: 800px;"
    v-model="args.value"
    :inputFields="args.inputFields"
    :title="args.title"
    @save="action('save')()"
    @input="action('input')()"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  value: true,
  inputFields: [
    {
      name: "firstName",
      rule: "required",
      label: "שם פרטי",
      value: "",
    },
    {
      name: "lastName",
      rule: "required",
      label: "שם משפחה",
      value: "",
    },
    {
      name: "phoneNumber",
      rule: "required",
      label: "טלפון",
      value: "0521234567",
    },
    {
      name: "favPokemon",
      type: "select",
      rule: "required",
      label: "פוקימון אהוב",
      choices: ["Pikachu", "Charizard", "Bulbasaur", "Snorlax"],
      value: "",
    },
  ],
  title: "אני כותרת",
}
