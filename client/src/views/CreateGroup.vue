<template>
  <div>
    <form-card
      v-model="fields"
      elevation="0"
      class="w-75 mx-auto"
      @valid="isFormValid = true"
      @invalid="isFormValid = false"
    />
    <v-btn
      class="white--text purple darken-3 mt-10 d-block mx-auto"
      data-testid="submit-button"
      :disabled="!isFormValid"
      @click="onSubmit"
      v-text="$t('userActions.save')"
    />
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
        rules: "required",
        label: i18n.t("groups.groupName"),
      },
      {
        name: "description",
        rules: "required",
        label: i18n.t("general.description"),
      },
      {
        name: "activityOrder",
        rules: "required",
        label: i18n.t("groups.parentProgram"),
        type: "select",
        choices: parentPrograms,
      },
    ]
    next(vm => (vm.fields = fields))
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
        const group = await this.createGroup(payload)
        this.showMessage(this.$t("groups.groupCreatedSuccessfully"))
        this.$router.push({ name: "AssignGroupConsumers", params: { groupSlug: group.slug } })
      } catch (err) {
        const message = Api.utils.parseResponseError(err)
        this.showMessage(message)
      }
    },
  },
}
</script>
