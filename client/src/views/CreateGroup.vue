<template>
  <div>
    <form-card
      focus
      v-model="fields"
      elevation="0"
      class="mx-auto"
      :class="{ 'w-75': $vuetify.breakpoint.smAndUp }"
      @valid="isFormValid = true"
      @invalid="isFormValid = false"
    />
    <v-btn
      class="white--text primary mt-10 d-block mx-auto"
      data-testid="submit-button"
      :disabled="!isFormValid"
      @click="onSubmit"
      v-text="$t('userActions.save')"
    />
  </div>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
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
    onSubmit: debounce(
      async function () {
        const data = { groupType: SERVER.programGroupTypes.standard }
        for (const f of this.fields) {
          data[f.name] = f.value
        }
        try {
          const group = await this.createGroup(data)
          this.showMessage(this.$t("groups.groupCreatedSuccessfully"))
          this.$router.push({
            name: "AssignGroupConsumers",
            params: { groupSlug: group.slug },
          })
        } catch (err) {
          const message = Api.utils.parseResponseError(err)
          this.showMessage(message)
        }
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
