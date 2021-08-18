<template>
  <div>
    <h2 v-text="$t('userActions.addStudentsToGroup')" />
    <table-rows-to-chips
      class="my-14"
      chips-label-header="name"
      v-model="selectedConsumers"
      :headers="tableHeaders"
      :items="availableConsumers"
      :loading="loading"
      @paginate="getAvailableConsumers"
    />
    <div class="mx-auto mt-10 text-center">
      <v-btn
        class="mx-3 white--text primary"
        data-testid="submit-button"
        :loading="btnLoading"
        @click="onSubmit"
      >
        {{ $t("userActions.save") }}
      </v-btn>
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
import store from "../vuex/store"
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
    const containerGroups = await store.dispatch(
      "programGroup/getGroupsByFilter",
      {
        group_type: SERVER.programGroupTypes.containerOnly,
        activity_order__slug: group.activityOrder,
      }
    )
    const groupSlugs = [...containerGroups, group].map(g => g.slug)
    const [availableConsumers, selectedConsumers] = await Promise.all([
      store.dispatch("programGroup/getConsumers", {
        groupSlugs,
        usePagination: true,
      }),
      store.dispatch("programGroup/getConsumers", {
        groupSlugs: [to.params.groupSlug],
        usePagination: false,
      }),
    ])
    next(vm => {
      vm.availableConsumers = availableConsumers
      vm.selectedConsumers = selectedConsumers
      vm.containerGroup = containerGroups[0]
    })
  },
  data() {
    return {
      loading: false,
      btnLoading: false,
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
    ...mapActions("programGroup", ["updateGroupConsumers", "getConsumers"]),
    ...mapActions("snackbar", ["showMessage"]),
    async getAvailableConsumers() {
      try {
        this.loading = true
        const groupSlugs = [this.containerGroup.slug, this.groupSlug]
        this.availableConsumers = await this.getConsumers({
          groupSlugs,
          usePagination: true,
        })
        this.loading = false
      } catch (err) {
        return this.showMessage(Api.utils.parseResponseError(err))
      }
    },
    onSubmit: debounce(
      async function () {
        this.btnLoading = true
        const consumerSlugs = this.selectedConsumers.map(c => c.slug)
        try {
          await this.updateGroupConsumers({
            groupSlug: this.groupSlug,
            consumerSlugs,
          })
        } catch (err) {
          this.btnLoading = false
          return this.showMessage(Api.utils.parseResponseError(err))
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
