<template>
  <div class="w-90 mx-auto mt-16">
    <h1 class="mb-5" v-text="$t('invite.inviteStudents')" />
    <h2
      class="pb-12"
      v-text="$t('invite.clickOnInviteStudentButtonToInviteNewStudentViaEmail')"
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
        :footerBtnOneText="`${$tc('invite.invite', 1)} ${$t(
          'general.student'
        )}`"
        :footerBtnTwoText="`${$tc('userActions.remove', 1)} ${$t(
          'general.student'
        )}`"
        :footer-btn-two-disabled="!selectedRows.length"
        @paginate="getStudents"
        @action-one-click="editStudent($event)"
        @footer-btn-one-click="addStudent"
        @footer-btn-two-click="handleDeleteRequest"
        @file-upload="importCSV"
        @file-download-request="exportCSV"
      >
        <template v-slot:item.profile.gender="{ item }">
          {{ $t(`gender.${item.profile.gender.toLowerCase()}`) }}
        </template>
      </pagination-complex-table>
      <add-student-dialog
        v-model="isDialogActive"
        :title="dialogTitle"
        :student="dialogStudent"
        :slug="dialogSlug"
        @save="getStudents"
      />
      <modal
        v-show="showInfoModal"
        @close="
          popupMsg = ''
          showInfoModal = false
        "
      >
        {{ popupMsg }}
      </modal>

      <modal
        v-show="showErrorModal"
        @close="
          popupMsg = ''
          showErrorModal = false
        "
        title="invite.uploadFileErrorTitle"
      >
        <div>{{ $t("invite.uploadFileErrorSummary") }}</div>
        <div style="padding-top: 2em">
          <span style="white-space: pre-line">
            {{ popupMsg }}
          </span>
        </div>
      </modal>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import { translateStatus } from "./helpers"
import Modal from "@/components/Modal"
import Api from "@/api"
import AddStudentDialog from "@/components/AddDialog/AddStudentDialog"
import PaginationComplexTable from "@/components/Tables/PaginationComplexTable"

export default {
  name: "InviteStudents",
  components: {
    Modal,
    AddStudentDialog,
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
        {
          text: this.$t("gender.gender"),
          value: "profile.gender",
          sortable: false,
        },
      ],
      isDialogActive: false,
      popupMsg: "",
      showInfoModal: false,
      showErrorModal: false,
      dialogStudent: {
        name: "",
        email: "",
        profile: {
          gender: "",
        },
      },
      dialogMode: "create",
      dialogSlug: null,
    }
  },

  computed: {
    dialogTitle() {
      if (this.dialogMode === "edit") {
        return `${this.$tc("userActions.edit", 1)} ${this.$t(
          "general.student"
        )}`
      }
      return `${this.$tc("invite.invite", 1)} ${this.$t("general.student")}`
    },
  },

  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("school", [
      "getStudentList",
      "deleteStudents",
      "addStudentsBulk",
      "getStudentsExportFile",
    ]),
    translateStatus,

    async getStudents() {
      this.loading = true
      this.items = await this.getStudentList({
        override: true,
        usePagination: true,
      })
      this.loading = false
    },

    async importCSV(file) {
      try {
        const added = await this.addStudentsBulk(file)
        this.getStudents()
        this.popupMsg = `${added.length} ${this.$t(
          "invite.consumersHasBeenInvitedViaEmailToJoinThePlatform"
        )}`
        this.showInfoModal = true
      } catch (err) {
        this.popupMsg = Api.utils.parseUploadUsersFileError(err)
        this.showErrorModal = true
      }
    },

    handleDeleteRequest: debounce(
      async function () {
        if (confirm(this.$t("confirm.AreYouSureYouWantToDelete?"))) {
          let slugs = this.selectedRows.map(row => row.slug)
          await this.deleteStudents(slugs)
          this.selectedRows = []
          this.getStudents()
          this.showMessage(this.$t("success.userDeletedSuccessfully"))
        }
      },
      500,
      { leading: true, trailing: false }
    ),

    editStudent(student) {
      this.dialogStudent = Object.assign({}, student)
      delete this.dialogStudent.slug
      this.dialogSlug = student.slug
      this.dialogMode = "edit"
      this.isDialogActive = true
    },

    addStudent() {
      this.dialogSlug = null
      this.dialogMode = "create"
      this.isDialogActive = true
    },

    exportCSV: debounce(
      function () {
        this.getStudentsExportFile({ usePagination: true })
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
