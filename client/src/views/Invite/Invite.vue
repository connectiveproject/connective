<template>
  <div class="wrapper mx-auto mt-16">
    <h1 class="mb-5">
      {{ `${$tc("invite.invite", 1)} ${$t("general.student")}` }}
    </h1>
    <h2 class="pb-12">
      {{ $t("invite.inviteStudentsToPlatformAndKeepTrackOfTheirStatus") }}
    </h2>
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
              getStudents()
            "
            @keyup.enter="
              tableProps.options.page = 1
              getStudents()
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
            <v-icon size="20" class="mr-2" @click="editStudent(item)">
              mdi-pencil
            </v-icon>
          </template>
          <template v-slot:item.profile.gender="{ item }">
            {{ $t(`gender.${item.profile.gender.toLowerCase()}`) }}
          </template>
          <!-- Pending Backend:
                    <template v-slot:item.createdOn="{ item }">
                        <span>{{ new Date(item.createdOn).toLocaleString() }}</span>
                    </template>
                    <template v-slot:item.status="{ item }">
                        <span>{{ translateStatus(item.status) }}</span>
                    </template>
                    -->
        </v-data-table>
        <v-card-actions class="grey lighten-5 mt-3">
          <v-btn
            @click="addStudent"
            :class="{ 'abs-center': $vuetify.breakpoint.smAndUp }"
            text
          >
            {{ `${$tc("invite.invite", 1)} ${$t("general.student")}` }}
          </v-btn>
          <v-spacer></v-spacer>
          <div class="pl-2">
            <v-btn
              text
              color="error"
              @click="handleDeleteRequest"
              :disabled="!selectedRows.length"
            >
              {{ `${$tc("userActions.remove", 1)} ${$t("general.student")}` }}
            </v-btn>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn @click="triggerCSVUpload" icon v-bind="attrs" v-on="on">
                  <v-icon color="purple darken-4">mdi-file-upload</v-icon>
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
                  <v-icon color="purple darken-4"
                    >mdi-file-download-outline</v-icon
                  >
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
      <add-student-dialog
        v-model="isDialogActive"
        :title="dialogTitle"
        :student="dialogStudent"
        :slug="dialogSlug"
        @save="getStudents"
      />
      <modal v-show="popupMsg !== ''" @close="popupMsg = ''">
        {{ popupMsg }}
      </modal>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import { exportCSV, validateStudentsArray, translateStatus } from "./helpers"
import Modal from "../../components/Modal"
import AddStudentDialog from "../../components/AddStudentDialog"

export default {
  components: {
    Modal,
    AddStudentDialog,
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
        serverItemsLength: this.$store.state.school.totalStudents,
        page: 1,
        pageCount: undefined,
        options: {},
        headers: [
          { text: "", value: "actions", sortable: false },
          { text: this.$t("general.name"), value: "name" },
          { text: this.$t("general.email"), value: "email" },
          { text: this.$t("gender.gender"), value: "profile.gender" },
          // Pending Backend:
          // { text: this.$t('general.date'), value: 'dateAdded' },
          // { text: this.$t('invite.invitationStatus'), value: 'status' },
        ],
      },

      csvFile: null,
      isDialogActive: false,
      popupMsg: "",

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
        this.getStudents()
      },
    },
  },

  methods: {
    ...mapActions("pagination", ["updatePagination"]),
    ...mapActions("school", [
      "getStudentList",
      "deleteStudents",
      "addStudents",
    ]),
    exportCSV,
    translateStatus,
    validateStudentsArray,

    async getStudents() {
      this.tableProps.loading = true
      let paginationOptions = {
        itemsPerPage: this.tableProps.options.itemsPerPage,
        page: this.tableProps.options.page,
        searchFilter: this.searchFilter,
        sort: {
          sortBy: this.tableProps.options.sortBy,
          sortDesc: this.tableProps.options.sortDesc,
        },
      }
      this.updatePagination(paginationOptions)
      this.tableProps.items = await this.getStudentList()
      this.tableProps.serverItemsLength = this.$store.state.school.totalStudents
      this.tableProps.loading = false
    },

    async importCSV() {
      // remove - Ronnie's decision
      // let studentsList = await Utils.csvToArray(this.csvFile)
      // let validationError = this.validateStudentsArray(studentList)
      // if (validationError) {
      //     return this.popupMsg = validationError
      // }
      try {
        await this.addStudents(this.csvFile)
        this.tableProps.options.page = 1
        this.getStudents()
        this.popupMsg = this.$t("general.detailsSuccessfullyUpdated")
      } catch {
        this.popupMsg = this.$t("errors.genericError")
      }
    },

    triggerCSVUpload() {
      document.getElementById("csvImportInput").click()
    },

    async handleDeleteRequest() {
      if (confirm(this.$t("general.AreYouSureYouWantToDelete"))) {
        let slugs = this.selectedRows.map(row => row.slug)
        await this.deleteStudents(slugs)
        this.selectedRows = []
        this.getStudents()
      }
    },

    editStudent(student) {
      this.dialogStudent = Object.assign({}, student)
      delete this.dialogStudent.slug
      delete this.dialogStudent.profile.slug
      this.dialogSlug = student.slug
      this.dialogMode = "edit"
      this.isDialogActive = true
    },

    addStudent() {
      this.dialogSlug = null
      this.dialogMode = "create"
      this.isDialogActive = true
    },
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
