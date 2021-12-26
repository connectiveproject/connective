<template>
  <v-row class="my-7" no-gutters>
    <v-col sm="11" lg="6">
      <form-card
        focus
        v-model="fields"
        elevation="0"
        @valid="isFormValid = true"
        @invalid="isFormValid = false"
      />
      <v-btn
        large
        class="white--text primary mt-10"
        data-testid="submit-button"
        :disabled="!isFormValid"
        @click="onSubmit"
        v-text="$t('userActions.save')"
      />
      <v-btn
        large
        outlined
        class="mt-10 mx-4"
        color="primary"
        @click="$router.go(-1)"
        v-text="$t('userActions.back')"
      />
    </v-col>
    <v-col sm="11" lg="6" v-if="!$vuetify.breakpoint.xs">
      <v-img :src="img" />
    </v-col>
  </v-row>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "@/vuex/store"
import i18n from "@/plugins/i18n"
import Api from "../api"
import { SERVER } from "../helpers/constants/constants"
import { CREATE_GROUP } from "../helpers/constants/images"
import FormCard from "../components/FormCard"

export default {
  components: { FormCard },
  async beforeRouteEnter(to, from, next) {
    // get all available programs & the number of students waiting to be assigned
    // construct form fields accordingly
    const approvedOrders = await store.dispatch("program/getApprovedOrdersList")
    const consumerRequestsPerOrder = await store.dispatch(
      "program/getTopConsumerRequestsStats",
      { top: 999 }
    )
    const parentPrograms = approvedOrders.map(order => {
      const filteredRequests = consumerRequestsPerOrder.filter(
        o => o.activityOrder === order.slug
      )
      let availableConsumers = 0
      if (filteredRequests.length) {
        availableConsumers = filteredRequests[0].consumerRequests
      }
      return {
        text: `${order.activityName} (${availableConsumers} ${i18n.t(
          "myActivity.studentsPendingAssignment"
        )})`,
        value: order.slug,
      }
    })
    const groupTypes = [
      {
        value: SERVER.programGroupTypes.standard,
        text: i18n.t("programGroupTypes.standard"),
      },
      {
        value: SERVER.programGroupTypes.noRegistration,
        text: i18n.t("programGroupTypes.noRegistration"),
      },
    ]

    const fields = [
      {
        name: "activityOrder",
        rules: "required",
        label: i18n.t("groups.parentProgram"),
        type: "select",
        choices: parentPrograms,
      },
      {
        name: "name",
        rules: "required",
        label: i18n.t("groups.groupName"),
      },
      {
        name: "description",
        rules: "required",
        label: i18n.t("general.description"),
        type: "textarea",
      },
      {
        name: "groupType",
        label: i18n.t("groups.groupType"),
        type: "select",
        value: SERVER.programGroupTypes.standard,
        choices: groupTypes,
      },
    ]
    next(vm => (vm.fields = fields))
  },
  data() {
    return {
      img: CREATE_GROUP,
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
          if (data.groupType == SERVER.programGroupTypes.noRegistration) {
            // no registration - no students to add ==> go to the group details page
            this.$router.push({
              name: "GroupDetail",
              params: { groupSlug: group.slug },
            })
          } else {
            // standard - go to add students
            this.$router.push({
              name: "AssignGroupConsumers",
              params: { groupSlug: group.slug },
            })
          }
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
