<template>
  <div class="wrapper mx-auto mt-16">
    <h1 class="mb-5" v-text="$t('invite.inviteStaff')" />
    <h2
      class="pb-12"
      v-text="$t('invite.inviteTheSchoolStaffToJoinThePlatform')"
    />
    <div class="mx-auto d-flex justify-center mt-10">
      <v-card elevation="3" class="mb-15">
        <v-card-title>
          <v-text-field
            v-model="searchFilter"
            append-icon="mdi-magnify"
            :label="$t('userActions.search')"
            single-line
            hide-details
            class="px-10 mt-5 mb-8"
            @click:append="
              tableProps.options.page = 1
              getCoordinators()
            "
            @keyup.enter="
              tableProps.options.page = 1
              getCoordinators()
            "
          />
        </v-card-title>
        <v-data-table
          show-select
          multi-sort
          v-bind.sync="tableProps"
          :no-data-text="$t('invite.clickTheButtonBelowToInviteUsers!')"
        >
          <template v-slot:item.actions="{ item }">
            <v-icon size="20" class="mr-2" @click="editCoordinator(item)">
              mdi-pencil
            </v-icon>
          </template>
        </v-data-table>
        <v-card-actions class="grey lighten-5 mt-3">
          <v-btn
            @click="addCoordinator"
            :class="{
              'glow-animation': !wasInviteBtnClicked,
              'abs-center': $vuetify.breakpoint.smAndUp,
            }"
            v-text="$t('invite.inviteStaffMember')"
            color="primary"
            outlined
          />
          <v-spacer></v-spacer>
          <div class="pl-2">
            <v-btn
              text
              color="error"
              @click="handleDeleteRequest"
              :disabled="!selectedRows.length"
              v-text="$t('invite.removeStaffMember')"
            />
            <v-tooltip bottom v-if="$vuetify.breakpoint.smAndUp">
              <template v-slot:activator="{ on, attrs }">
                <v-btn @click="triggerCSVUpload" icon v-bind="attrs" v-on="on">
                  <v-icon color="primary">mdi-file-upload</v-icon>
                </v-btn>
              </template>
              <span class="px-3">{{ $t("userActions.import") }} CSV</span>
            </v-tooltip>
            <v-tooltip bottom v-if="$vuetify.breakpoint.smAndUp">
              <template v-slot:activator="{ on, attrs }">
                <v-btn @click="exportCSV" icon v-bind="attrs" v-on="on">
                  <v-icon color="primary">mdi-file-download-outline</v-icon>
                </v-btn>
              </template>
              <span class="px-3">{{ $t("userActions.export") }}</span>
            </v-tooltip>
          </div>
        </v-card-actions>
      </v-card>
      <v-file-input
        id="csvImportInput"
        class="d-none"
        type="file"
        accept=".csv"
        v-model="csvFile"
      >
      </v-file-input>
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

export default {
  components: {
    Modal,
    AddCoordinatorDialog,
  },

  data() {
    return {
      searchFilter: "",
      selectedRows: [],
      wasInviteBtnClicked: false,
      tableProps: {
        items: [],
        itemKey: "email",
        loading: false,
        loadingText: this.$t("general.loading"),
        serverItemsLength: this.$store.state.school.totalCoordinators,
        page: 1,
        pageCount: undefined,
        options: {},
        headers: [
          { text: "", value: "actions", sortable: false },
          { text: this.$t("general.name"), value: "name" },
          { text: this.$t("general.email"), value: "email" },
        ],
      },

      csvFile: null,
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

  watch: {
    csvFile() {
      if (this.csvFile) {
        // on upload, run the import chain
        this.importCSV()
      }
    },
    "tableProps.options": {
      // re-fetch data on user request (e.g., sort, next page)
      deep: true,
      handler() {
        this.getCoordinators()
      },
    },
  },

  methods: {
    ...mapActions("pagination", ["updatePagination"]),
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("school", [
      "getCoordinatorList",
      "deleteCoordinators",
      "addCoordinatorsBulk",
      "getCoordinatorsExportFile",
    ]),
    translateStatus,

    async getCoordinators() {
      this.tableProps.loading = true
      let paginationOptions = {
        itemsPerPage: this.tableProps.options.itemsPerPage,
        page: this.tableProps.options.page,
        searchFilter: this.searchFilter,
        sortBy: this.tableProps.options.sortBy,
        sortDesc: this.tableProps.options.sortDesc,
      }
      this.updatePagination(paginationOptions)
      this.tableProps.items = await this.getCoordinatorList()
      this.tableProps.serverItemsLength =
        this.$store.state.school.totalCoordinators
      this.tableProps.loading = false
    },

    async importCSV() {
      try {
        const added = await this.addCoordinatorsBulk(this.csvFile)
        this.tableProps.options.page = 1
        this.getCoordinators()
        this.popupMsg = `${added.length} ${this.$t(
          "invite.coordinatorsHasBeenInvitedViaEmailToJoinThePlatform"
        )}`
        this.csvFile = null
      } catch (err) {
        this.popupMsg = Api.utils.parseResponseError(err)
        this.csvFile = null
      }
    },

    triggerCSVUpload() {
      document.getElementById("csvImportInput").click()
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
      this.wasInviteBtnClicked = true
      this.dialogSlug = null
      this.dialogMode = "create"
      this.isDialogActive = true
    },

    exportCSV: debounce(
      function () {
        this.getCoordinatorsExportFile()
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>

<style lang="scss" scoped>
.wrapper {
  width: 90%;
}

.abs-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
</style>
