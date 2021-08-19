<template>
  <div class="w-90 mx-auto mt-16">
    <h1 class="mb-5" v-text="$t('invite.inviteVendors')" />
    <h2
      class="pb-12"
      v-text="$t('invite.inviteAdditionalVendorsToJoinThePlatform')"
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
        :footerBtnOneText="$t('invite.inviteUser')"
        :footerBtnTwoText="$t('invite.removeUser')"
        :footer-btn-two-disabled="!selectedRows.length"
        @paginate="getVendors"
        @action-one-click="editVendor($event)"
        @footer-btn-one-click="addVendor"
        @footer-btn-two-click="handleDeleteRequest"
        @file-upload="importCSV"
        @file-download-request="exportCSV"
      />
      <add-vendor-dialog
        v-model="isDialogActive"
        :title="dialogTitle"
        :vendor="dialogVendor"
        :slug="dialogSlug"
        @save="getVendors"
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
import AddVendorDialog from "../../components/AddDialog/AddVendorDialog"
import PaginationComplexTable from "../../components/Tables/PaginationComplexTable"

export default {
  name: "InviteVendors",
  components: {
    Modal,
    AddVendorDialog,
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
      dialogVendor: {
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
        return this.$t("invite.editVendor")
      }
      return this.$t("invite.inviteVendor")
    },
  },

  methods: {
    ...mapActions("pagination", ["updatePagination"]),
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("organization", [
      "getVendorList",
      "deleteVendors",
      "addVendors",
    ]),
    translateStatus,

    async getVendors() {
      this.loading = true
      this.items = await this.getVendorList({
        override: true,
        usePagination: true,
      })
      this.loading = false
    },

    async importCSV(file) {
      try {
        const added = await this.addVendorsBulk(file)
        this.getVendors()
        this.popupMsg = `${added.length} ${this.$t(
          "invite.VendorsHasBeenInvitedViaEmailToJoinThePlatform"
        )}`
      } catch (err) {
        this.popupMsg = Api.utils.parseResponseError(err)
      }
    },

    handleDeleteRequest: debounce(
      async function () {
        if (confirm(this.$t("confirm.AreYouSureYouWantToDelete?"))) {
          let slugs = this.selectedRows.map(row => row.slug)
          await this.deleteVendors(slugs)
          this.selectedRows = []
          this.getVendors()
          this.showMessage(this.$t("success.userDeletedSuccessfully"))
        }
      },
      500,
      { leading: true, trailing: false }
    ),

    editVendor(vendor) {
      this.dialogVendor = Object.assign({}, vendor)
      delete this.dialogVendor.slug
      this.dialogSlug = vendor.slug
      this.dialogMode = "edit"
      this.isDialogActive = true
    },

    addVendor() {
      this.dialogSlug = null
      this.dialogMode = "create"
      this.isDialogActive = true
    },

    exportCSV: debounce(
      function () {
        this.getVendorsExportFile({ usePagination: true })
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
