<template>
  <div>
    <h1 class="pb-4" v-text="$t('groups.vendorgroups')" />
    <h2 v-text="$t('edit me subtitle')" class="pb-12" />
    <actions-table
      introjs="actions-table"
      class="mb-10"
      actions-title="shibutz madrih"
      action-one-icon="mdi-account-edit"
      action-one-icon-color="primary"
      :action-one-icon-tooltip="`${$t('CHANGE MEEEE')} / ${$t(
        'userActions.cancel'
      )}`"
      :totalActions="1"
      :headers="headers"
      :items="readableGroupList"
      @action-one-click="triggerInstructorAssignModal"
    />
    <form-dialog
      v-model="isDialogOpen"
      :title="$tc('general.chooseinstruvtir', 0)"
      :subtitle="`${$t('events.attention!change meeeee')}.`"
      :input-fields="assignInstructorDialogFields"
      @save="assignInstructor"
    />
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Api from "../api"
// import Utils from "../helpers/utils"
import { SERVER } from "../helpers/constants/constants"
import ActionsTable from "../components/ActionsTable"
// import ModalApprove from "../components/ModalApprove"
import FormDialog from "../components/FormDialog"
// import introjsSubscribeMixin from "../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "VendorGroupsTable",
  components: { ActionsTable, FormDialog },
  // mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("vendorProgramGroup/getGroupList", {
      groupType: SERVER.programGroupTypes.standard,
      override: true,
    })
    next()
  },
  async mounted() {
    const instructors = await this.getInstructorList()
    this.instructorList = instructors.map(instructor => ({
      value: instructor.slug,
      text: instructor.name,
    }))
  },
  computed: {
    ...mapState("vendorProgramGroup", ["groupList"]),
    assignInstructorDialogFields() {
      return [
        {
          name: "instructor",
          rule: "required",
          label: this.$t("instructooooooor"),
          value: "",
          type: "select",
          choices: this.instructorList,
        },
      ]
    },

    readableGroupList() {
      return this.groupList.map(group => ({
        ...group,
        totalConsumers: group.consumers.length,
      }))
    },
  },
  data() {
    return {
      instructorList: ["loading..."],
      groupForInstructorAssignment: null,
      isDialogOpen: false,
      isDenyFormDialogActive: false,
      headers: [
        { text: this.$t("groups.groupName"), value: "name" },
        { text: this.$t("groups.activityName"), value: "activityName" },
        { text: this.$t("groups.totalConsumers"), value: "totalConsumers" },
        { text: this.$t("groups.description"), value: "description" }, // trim
        { text: this.$t("groups.instructor"), value: "instructorName" },
      ],
    }
  },
  methods: {
    ...mapActions("vendorProgramGroup", ["updateGroup"]),
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("organization", ["getInstructorList"]),
    triggerInstructorAssignModal: debounce(
      async function (group) {
        this.groupForInstructorAssignment = group
        this.isDialogOpen = true
      },
      500,
      { leading: true, trailing: false }
    ),

    async assignInstructor({ instructor }) {
      try {
        const groupSlug = this.groupForInstructorAssignment.slug
        await this.updateGroup({ groupSlug, data: { instructor } })
        this.showMessage("ADDED!!")
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
}
</script>
