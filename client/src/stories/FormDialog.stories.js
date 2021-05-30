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
      label: "First Name",
      value: "",
    },
    {
      name: "lastName",
      rule: "required",
      label: "Last Name",
      value: "",
    },
    {
      name: "phoneNumber",
      rule: "required",
      label: "Phone",
      value: "0521234567",
    },
    {
      name: "favPokemon",
      rule: "required",
      label: "Favorite Pokemon",
      value: "Pikachu",
    },
  ],
  title: "Title",
}
