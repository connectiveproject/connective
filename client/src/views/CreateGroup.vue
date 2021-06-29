<template>
  <div>
    <form-card
      v-model="fields"
      elevation="0"
      class="w-75 mx-auto"
      @valid="isFormValid = true"
      @invalid="isFormValid = false"
    />
    <v-btn :disabled="!isFormValid" @click="onSubmit">Submit</v-btn>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import store from "../vuex/store"
import i18n from "../plugins/i18n"
import Api from "../api"
import { SERVER } from "../helpers/constants/constants"
import FormCard from "../components/FormCard"

export default {
  components: { FormCard },
  async beforeRouteEnter(to, from, next) {
    const approvedOrders = await store.dispatch("program/getApprovedOrdersList")
    const parentPrograms = approvedOrders.map(order => ({
      text: order.activityName,
      value: order.slug,
    }))
    const fields = [
      {
        name: "name",
        rule: "required",
        label: i18n.t("groups.groupName"),
      },
      {
        name: "description",
        rule: "required",
        label: i18n.t("general.description"),
      },
      {
        name: "activityOrder",
        rule: "required",
        label: i18n.t("groups.parentProgram"),
        type: "select",
        choices: parentPrograms,
      },
    ]
    next(vm => vm.fields = fields)
  },
  data() {
    return {
      fields: [],
      isFormValid: false,
    }
  },
  methods: {
    ...mapActions("programGroup", ["createGroup"]),
    ...mapActions("snackbar", ["showMessage"]),
    async onSubmit() {
      const payload = { groupType: SERVER.programGroupTypes.standard }
      for (const f of this.fields) {
        payload[f.name] = f.value
      }
      try {
        await this.createGroup(payload)
        this.showMessage(this.$t("groupCreatedSuccessfully"))
        this.$router.push({ name: "assignGroupConsumers" })
      } catch (err) {
        const message = Api.utils.parseResponseError(err)
        this.showMessage(message)
      }
    },
  },
}
</script>
