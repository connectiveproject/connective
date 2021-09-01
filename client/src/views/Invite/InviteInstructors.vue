<template>
  <div class="w-90 mx-auto mt-16">
    <h1 class="mb-5" v-text="$t('invite.inviteInstructors')" />
    <h2
      class="pb-12"
      v-text="$t('invite.clickOnInviteUserButtonToInviteNewInstructorViaEmail')"
    />
    <div class="mx-auto d-flex justify-center mt-10 mb-3">
      <pagination-complex-table
        show-select
        actions-first
        v-model="selectedRows"
        item-key="email"
        action-one-icon="mdi-pencil"
        action-one-icon-color="grey darken-2"
        hide-footer-icons
        :headers="headers"
        :items="items"
        :loading="loading"
        :totalActions="1"
        :no-data-text="$t('invite.clickTheButtonBelowToInviteUsers!')"
        :action-one-icon-tooltip="$tc('userActions.edit', 2)"
        :footerBtnOneText="$t('invite.inviteUser')"
        :footerBtnTwoText="$t('invite.removeUser')"
        :footer-btn-two-disabled="!selectedRows.length"
        @paginate="getInstructors"
        @action-one-click="editInstructor($event)"
        @footer-btn-one-click="addInstructor"
        @footer-btn-two-click="handleDeleteRequest"
        @file-upload="importCSV"
        @file-download-request="exportCSV"
      />
      <add-instructor-dialog
        v-model="isDialogActive"
        :title="dialogTitle"
        :instructor="dialogInstructor"
        :slug="dialogSlug"
        @save="getInstructors"
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
import AddInstructorDialog from "../../components/AddDialog/AddInstructorDialog"
import PaginationComplexTable from "../../components/Tables/PaginationComplexTable"

export default {
  name: "InviteInstructors",
  components: {
    Modal,
    AddInstructorDialog,
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
      dialogInstructor: {
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
        return this.$t("invite.editInstructor")
      }
      return this.$t("invite.inviteInstructor")
    },
  },

  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("organization", [
      "getInstructorList",
      "deleteInstructors",
      "addInstructors",
    ]),
    translateStatus,

    async getInstructors() {
      this.loading = true
      this.items = await this.getInstructorList({
        override: true,
        usePagination: true,
      })
      this.loading = false
    },

    async importCSV(file) {
      try {
        const added = await this.addInstructorsBulk(file)
        this.getInstructors()
        this.popupMsg = `${added.length} ${this.$t(
          "invite.instructorsHasBeenInvitedViaEmailToJoinThePlatform"
        )}`
      } catch (err) {
        this.popupMsg = Api.utils.parseResponseError(err)
      }
    },

    handleDeleteRequest: debounce(
      async function () {
        if (confirm(this.$t("confirm.AreYouSureYouWantToDelete?"))) {
          let slugs = this.selectedRows.map(row => row.slug)
          await this.deleteInstructors(slugs)
          this.selectedRows = []
          this.getInstructors()
          this.showMessage(this.$t("success.userDeletedSuccessfully"))
        }
      },
      500,
      { leading: true, trailing: false }
    ),

    editInstructor(instructor) {
      this.dialogInstructor = Object.assign({}, instructor)
      delete this.dialogInstructor.slug
      this.dialogSlug = instructor.slug
      this.dialogMode = "edit"
      this.isDialogActive = true
    },

    addInstructor() {
      this.dialogSlug = null
      this.dialogMode = "create"
      this.isDialogActive = true
    },

    exportCSV: debounce(
      function () {
        this.getInstructorsExportFile({ usePagination: true })
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
