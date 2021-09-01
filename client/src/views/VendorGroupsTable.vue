<template>
  <div>
    <h1 class="pb-4" v-text="$t('myActivity.myGroups')" />
    <h2
      v-text="$t('groups.browseYourGroupsAndAssignInstructors')"
      class="pb-12"
    />
    <pagination-actions-table
      introjs="actions-table"
      class="mb-10"
      action-one-icon="mdi-account-edit"
      action-one-icon-color="primary"
      :loading="loading"
      :actions-title="$t('groups.instructorAssignment')"
      :action-one-icon-tooltip="$t('groups.instructorAssignment')"
      :totalActions="1"
      :headers="headers"
      :items="readableGroupList"
      :no-data-text="$t('errors.noGroupsFound')"
      @paginate="getGroups"
      @action-one-click="triggerInstructorAssignModal"
    />
    <form-dialog
      v-model="isDialogOpen"
      :title="$t('groups.instructorAssignment')"
      :subtitle="$t('groups.chooseInstructorForTheGroup')"
      :input-fields="assignInstructorDialogFields"
      @save="assignInstructor"
    />
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "@/vuex/store"
import Api from "../api"
import { SERVER } from "../helpers/constants/constants"
import PaginationActionsTable from "../components/Tables/PaginationActionsTable"
import FormDialog from "../components/FormDialog"
import introjsSubscribeMixin from "../mixins/introJs/introjsSubscribeMixin"
import { trimText } from "../filters"

export default {
  name: "VendorGroupsTable",
  components: { PaginationActionsTable, FormDialog },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    // change pagination only for the following query
    const itemsPerPage = store.state.pagination.itemsPerPage
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 500 })
    await store.dispatch("organization/getInstructorList", {
      usePagination: true,
    })
    await store.dispatch("pagination/updatePagination", { itemsPerPage })
    next()
  },
  computed: {
    ...mapState("vendorProgramGroup", ["groupList"]),
    ...mapState("organization", ["instructorList"]),
    instrcutors() {
      return this.instructorList.map(instructor => ({
        value: instructor.slug,
        text: instructor.name,
      }))
    },
    assignInstructorDialogFields() {
      return [
        {
          name: "instructor",
          rule: "required",
          label: this.$t("general.instructor"),
          value: "",
          type: "select",
          choices: this.instrcutors,
        },
      ]
    },

    readableGroupList() {
      return this.groupList.map(group => ({
        ...group,
        description: trimText(group.description, 45),
        totalConsumers: group.consumers.length,
      }))
    },
  },
  data() {
    return {
      loading: false,
      groupForInstructorAssignment: null,
      isDialogOpen: false,
      isDenyFormDialogActive: false,
      headers: [
        { text: this.$t("groups.groupName"), value: "name" },
        {
          text: this.$t("program.programName"),
          value: "activityName",
          sortable: false,
        },
        { text: this.$t("general.schoolName"), value: "schoolName", sortable: false, },
        {
          text: this.$t("myActivity.studentsNumberInGroup"),
          value: "totalConsumers",
          sortable: false,
        },
        { text: this.$t("myActivity.groupDescription"), value: "description" },
        {
          text: this.$t("general.instructor"),
          value: "instructorName",
          sortable: false,
        },
      ],
    }
  },
  methods: {
    ...mapActions("vendorProgramGroup", ["updateGroup", "getGroupList"]),
    ...mapActions("snackbar", ["showMessage"]),
    triggerInstructorAssignModal: debounce(
      async function (group) {
        this.groupForInstructorAssignment = group
        this.isDialogOpen = true
      },
      500,
      { leading: true, trailing: false }
    ),
    async getGroups() {
      this.loading = true
      await this.getGroupList({
        groupType: SERVER.programGroupTypes.standard,
        override: true,
        usePagination: true,
      })

      this.loading = false
    },
    async assignInstructor({ instructor }) {
      try {
        const groupSlug = this.groupForInstructorAssignment.slug
        await this.updateGroup({ groupSlug, data: { instructor } })
        this.showMessage(
          this.$t("success.instructorAssignedToGroupSuccessfully")
        )
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
}
</script>
