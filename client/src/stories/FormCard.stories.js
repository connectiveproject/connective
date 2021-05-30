import FormCard from "../components/FormCard.vue"

export default {
  title: "FormCard",
  component: FormCard,
}

const Template = args => ({
  components: { FormCard },
  data: () => ({ args }),
  template: `
    <form-card
    class="mx-auto"
    style="width: 800px;"
    v-model="args.value"
    elevation="args.elevation"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  value: [
    {
      name: "firstName",
      rule: "required",
      label: "First Name",
      value: ""
    },
    {
      name: "lastName",
      rule: "required",
      label: "Last Name",
      value: ""
    },
    {
      name: "phoneNumber",
      rule: "required",
      label: "Phone",
      value: "0521234567"
    },
  ],
  elevation: 2,
}
