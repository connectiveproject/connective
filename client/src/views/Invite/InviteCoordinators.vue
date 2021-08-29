<template>
  <div class="w-90 mx-auto mt-16">
    <h1 class="mb-5" v-text="$t('invite.inviteStaff')" />
    <h2
      class="pb-12"
      v-text="
        $t('invite.clickOnInviteStaffButtonToInviteNewStaffMemberViaEmail')
      "
    />
    <div class="mx-auto d-flex justify-center mt-10 mb-3">
      <pagination-complex-table
        show-select
        actions-first
        v-model="selectedRows"
        item-key="email"
        action-one-icon="mdi-pencil"
        action-one-icon-color="grey darken-2"
        :headers="headers"
        :items="items"
        :loading="loading"
        :totalActions="1"
        :no-data-text="$t('invite.clickTheButtonBelowToInviteUsers!')"
        :action-one-icon-tooltip="$tc('userActions.edit', 2)"
        :footerBtnOneText="$t('invite.inviteStaffMember')"
        :footerBtnTwoText="$t('invite.removeStaffMember')"
        :footer-btn-two-disabled="!selectedRows.length"
        @paginate="getCoordinators"
        @action-one-click="editCoordinator($event)"
        @footer-btn-one-click="addCoordinator"
        @footer-btn-two-click="handleDeleteRequest"
        @file-upload="importCSV"
        @file-download-request="exportCSV"
      />
      <add-coordinator-dialog
        v-model="isDialogActive"
        :title="dialogTitle"
        :coordinator="dialogCoordinator"
        :slug="dialogSlug"
        @save="getCoordinators"
      />
      <modal v-show="popupMsg !== ''" @close="popupMsg = ''">
        {{ popupMsg }}
      </modal>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import Api from "../../api"
import { translateStatus } from "./helpers"
import Modal from "../../components/Modal"
import AddCoordinatorDialog from "../../components/AddDialog/AddCoordinatorDialog"
import PaginationComplexTable from "../../components/Tables/PaginationComplexTable"

export default {
  name: "InviteCoordinators",
  components: {
    Modal,
    AddCoordinatorDialog,
    PaginationComplexTable,
  },
  data() {
    return {
      loading: false,
      items: [],
      selectedRows: [],
      headers: [
        { text: this.$t("general.name"), value: "name" },
        { text: this.$t("general.email"), value: "email" },
      ],
      isDialogActive: false,
      popupMsg: "",
      dialogCoordinator: {
        name: "",
        email: "",
      },
      dialogMode: "create",
      dialogSlug: null,
    }
  },

  computed: {
    dialogTitle() {
      if (this.dialogMode === "edit") {
        return this.$t("invite.editStaffMember")
      }
      return this.$t("invite.inviteStaffMember")
    },
  },

  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("school", [
      "getCoordinatorList",
      "deleteCoordinators",
      "addCoordinatorsBulk",
      "getCoordinatorsExportFile",
    ]),
    translateStatus,

    async getCoordinators() {
      this.loading = true
      this.items = await this.getCoordinatorList({
        override: true,
        usePagination: true,
      })
      this.loading = false
    },

    async importCSV(file) {
      try {
        const added = await this.addCoordinatorsBulk(file)
        this.getCoordinators()
        this.popupMsg = `${added.length} ${this.$t(
          "invite.coordinatorsHasBeenInvitedViaEmailToJoinThePlatform"
        )}`
      } catch (err) {
        this.popupMsg = Api.utils.parseResponseError(err)
      }
    },

    handleDeleteRequest: debounce(
      async function () {
        if (confirm(this.$t("confirm.AreYouSureYouWantToDelete?"))) {
          let slugs = this.selectedRows.map(row => row.slug)
          await this.deleteCoordinators(slugs)
          this.selectedRows = []
          this.getCoordinators()
          this.showMessage(this.$t("success.userDeletedSuccessfully"))
        }
      },
      500,
      { leading: true, trailing: false }
    ),

    editCoordinator(coordinator) {
      this.dialogCoordinator = Object.assign({}, coordinator)
      delete this.dialogCoordinator.slug
      this.dialogSlug = coordinator.slug
      this.dialogMode = "edit"
      this.isDialogActive = true
    },

    addCoordinator() {
      this.dialogSlug = null
      this.dialogMode = "create"
      this.isDialogActive = true
    },

    exportCSV: debounce(
      function () {
        this.getCoordinatorsExportFile({ usePagination: true })
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
