<template>
  <div class="mx-auto">
    <h1 class="mb-5" v-text="$t('invite.inviteVendors')" />
    <h2
      class="pb-12"
      v-text="$t('invite.inviteAdditionalVendorsToJoinThePlatform')"
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
              getVendors()
            "
            @keyup.enter="
              tableProps.options.page = 1
              getVendors()
            "
          />
        </v-card-title>
        <v-data-table
          show-select
          multi-sort
          v-bind.sync="tableProps"
          v-model="selectedRows"
        >
          <template v-slot:item.actions="{ item }">
            <v-icon size="20" class="mr-2" @click="editVendor(item)">
              mdi-pencil
            </v-icon>
          </template>
        </v-data-table>
        <v-card-actions class="grey lighten-5 mt-3">
          <v-btn
            @click="addVendor"
            :class="{ 'abs-center': $vuetify.breakpoint.smAndUp }"
            text
            v-text="$t('invite.inviteUser')"
          />
          <v-spacer></v-spacer>
          <div class="pl-2">
            <v-btn
              text
              color="error"
              @click="handleDeleteRequest"
              :disabled="!selectedRows.length"
              v-text="$t('invite.removeUser')"
            />
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn @click="triggerCSVUpload" icon v-bind="attrs" v-on="on">
                  <v-icon color="primary">mdi-file-upload</v-icon>
                </v-btn>
              </template>
              <span class="px-3">{{ $t("userActions.import") }} CSV</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  @click="exportCSV(tableProps.items)"
                  icon
                  v-bind="attrs"
                  v-on="on"
                >
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
import { exportCSV, translateStatus } from "./helpers"
import Modal from "../../components/Modal"
import AddVendorDialog from "../../components/AddDialog/AddVendorDialog"

export default {
  components: {
    Modal,
    AddVendorDialog,
  },

  data() {
    return {
      searchFilter: "",
      selectedRows: [],
      tableProps: {
        items: [],
        itemKey: "email",
        loading: false,
        loadingText: this.$t("general.loading"),
        serverItemsLength: this.$store.state.organization.totalVendors,
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
        this.getVendors()
      },
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
    exportCSV,
    translateStatus,

    async getVendors() {
      this.tableProps.loading = true
      let paginationOptions = {
        itemsPerPage: this.tableProps.options.itemsPerPage,
        page: this.tableProps.options.page,
        searchFilter: this.searchFilter,
        sortBy: this.tableProps.options.sortBy,
        sortDesc: this.tableProps.options.sortDesc,
      }
      this.updatePagination(paginationOptions)
      this.tableProps.items = await this.getVendorList()
      this.tableProps.serverItemsLength =
        this.$store.state.organization.totalVendors
      this.tableProps.loading = false
    },

    async importCSV() {
      try {
        await this.addVendors(this.csvFile)
        this.tableProps.options.page = 1
        this.getVendors()
        this.popupMsg = this.$t("general.detailsSuccessfullyUpdated")
      } catch {
        this.popupMsg = this.$t("errors.genericError")
      }
    },

    triggerCSVUpload() {
      document.getElementById("csvImportInput").click()
    },

    async handleDeleteRequest() {
      if (confirm(this.$t("confirm.AreYouSureYouWantToDelete?"))) {
        let slugs = this.selectedRows.map(row => row.slug)
        await this.deleteVendors(slugs)
        this.selectedRows = []
        this.getVendors()
        this.showMessage(this.$t("success.userDeletedSuccessfully"))
      }
    },

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
  },
}
</script>

<style lang="scss" scoped>
.abs-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
</style>