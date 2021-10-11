<template>
  <div>
    <h2 v-text="$t('userActions.addStudentsToGroup')" />
    <table-rows-to-chips
      class="my-14"
      hide-search
      disable-sort
      chips-label-header="name"
      v-model="selectedConsumers"
      :headers="tableHeaders"
      :items="availableConsumers"
      :loading="loading"
      @paginate="getAvailableConsumers"
    >
      <template slot="footer.prepend">
        <v-btn
          class="px-5"
          color="primary"
          @click="openUnlistedConsumersDialog"
          v-text="$t('groups.studentsWhichAreNotListed')"
        />
      </template>
    </table-rows-to-chips>

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
    <v-dialog v-model="showUnlistedConsumersDialog" width="500">
      <pagination-complex-table
        show-select
        actions-first
        v-model="selectedUnlistedConsumers"
        item-key="slug"
        action-one-icon-color="grey darken-2"
        hide-footer-icons
        :headers="dialogTableHeaders"
        :items="dialogStudents"
        :loading="dialogLoading"
        :totalActions="0"
        :no-data-text="
          $t('invite.?????????????????????????????????????????????console.log(')
        "
        :footer-btn-one-text="$t('userActions.addStudentsToGroup')"
        :footer-btn-one-disabled="!selectedUnlistedConsumers.length"
        @paginate="getDialogStudents"
        @footer-btn-one-click="addDialogConsumersToGroup"
      />
    </v-dialog>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "@/vuex/store"
import Api from "@/api"
import { SERVER } from "@/helpers/constants/constants"
import TableRowsToChips from "@/components/TableRowsToChips"
import PaginationComplexTable from "@/components/Tables/PaginationComplexTable"

export default {
  components: { TableRowsToChips, PaginationComplexTable },
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
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 500 })
    const [selectedConsumers, containerGroups] = await Promise.all([
      store.dispatch("programGroup/getConsumers", {
        groupSlugs: [to.params.groupSlug],
        usePagination: true,
      }),
      store.dispatch("programGroup/getGroupsByFilter", {
        group_type: SERVER.programGroupTypes.containerOnly,
        activity_order__slug: group.activityOrder,
      }),
    ])
    next(vm => {
      vm.selectedConsumers = selectedConsumers
      vm.containerGroupSlugs = containerGroups.map(g => g.slug)
    })
  },
  data() {
    return {
      loading: false,
      btnLoading: false,
      selectedConsumers: [],
      availableConsumers: [],
      containerGroupSlugs: null,
      tableHeaders: [
        { text: this.$t("general.name"), value: "name" },
        { text: this.$t("general.email"), value: "email" },
      ],
      //////////// console.log("rename and move to a different component")
      //////////// console.log("check why moving between table pages does not work")
      showUnlistedConsumersDialog: false,
      selectedUnlistedConsumers: [],
      dialogStudents: [],
      dialogTableHeaders: [{ text: this.$t("general.name"), value: "name" }],
      dialogLoading: false,
    }
  },
  methods: {
    ...mapActions("programGroup", ["updateGroupConsumers", "getConsumers"]),
    ...mapActions("school", ["getStudentList"]),
    ...mapActions("snackbar", ["showMessage"]),
    async getAvailableConsumers() {
      try {
        this.loading = true
        const groupSlugs = [...this.containerGroupSlugs, this.groupSlug]
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
    async openUnlistedConsumersDialog() {
      await this.getDialogStudents()
      this.showUnlistedConsumersDialog = true
    },
    async getDialogStudents() {
      this.dialogLoading = true
      this.dialogStudents = await this.getStudentList({
        override: true,
        usePagination: true,
      })
      this.dialogLoading = false
    },
    addDialogConsumersToGroup() {
      return
    }
  },
}
</script>
