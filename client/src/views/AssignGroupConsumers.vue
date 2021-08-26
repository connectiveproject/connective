<template>
  <div>
    <table-rows-to-chips
      class="my-14"
      chipsLabelHeader="name"
      v-model="selectedConsumers"
      :headers="tableHeaders"
      :items="availableConsumers"
    />
    <div class="mx-auto mt-10 text-center">
      <v-btn
        class="mx-3 white--text primary"
        data-testid="submit-button"
        @click="onSubmit"
        v-text="$t('userActions.save')"
      />
      <v-btn
        class="mx-3 white--text"
        color="primary"
        outlined
        v-text="$t('userActions.back')"
        @click="$router.go(-1)"
      />
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "@/vuex/store"
import Api from "../api"
import { SERVER } from "../helpers/constants/constants"
import TableRowsToChips from "../components/TableRowsToChips"

export default {
  components: { TableRowsToChips },
  props: {
    groupSlug: {
      type: String,
      required: true,
    },
  },
  async beforeRouteEnter(to, from, next) {
    // fetch assigned & unassigned consumers
    const group = await store.dispatch(
      "programGroup/getGroup",
      to.params.groupSlug
    )
    const groupConsumers = await store.dispatch(
      "programGroup/getConsumers",
      to.params.groupSlug
    )
    const containerGroups = await store.dispatch(
      "programGroup/getGroupsByFilter",
      {
        group_type: SERVER.programGroupTypes.containerOnly,
        activity_order__slug: group.activityOrder,
      }
    )
    let unassignedConsumers = []
    if (containerGroups.length) {
      unassignedConsumers = await store.dispatch(
        "programGroup/getConsumers",
        containerGroups[0].slug
      )
    }
    next(vm => {
      vm.selectedConsumers = groupConsumers
      vm.availableConsumers = [...groupConsumers, ...unassignedConsumers]
      vm.containerGroup = containerGroups[0]
    })
  },
  data() {
    return {
      selectedConsumers: [],
      availableConsumers: [],
      containerGroup: null,
      tableHeaders: [
        { text: this.$t("general.name"), value: "name" },
        { text: this.$t("general.email"), value: "email" },
      ],
    }
  },
  methods: {
    ...mapActions("programGroup", ["updateGroupConsumers"]),
    ...mapActions("snackbar", ["showMessage"]),
    onSubmit: debounce(
      async function () {
        const consumerSlugs = this.selectedConsumers.map(c => c.slug)
        if (this.containerGroup) {
          try {
            await this.updateGroupConsumers({
              groupSlug: this.groupSlug,
              consumerSlugs,
            })
          } catch (err) {
            return this.showMessage(Api.utils.parseResponseError(err))
          }
        }
        this.showMessage(this.$t("general.detailsSuccessfullyUpdated"))
        this.$router.push({
          name: "GroupDetail",
          params: { groupSlug: this.groupSlug },
        })
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
