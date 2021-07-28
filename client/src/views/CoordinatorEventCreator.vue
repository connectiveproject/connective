<template>
  <v-row class="pa-10">
    <v-col class="mx-auto" sm="11" lg="9">
      <h1 class="pb-8" v-text="$t('events.eventsCreation')" />
      <radio-group
        class="pa-0"
        v-model="recurrence"
        :title="`${$t('time.recurrence')}:`"
        :choices="recurrenceChoices"
        row
      />
      <date-input v-model="startDate" :label="$t('time.startDate')" />
      <time-input v-model="startTime" :label="$t('time.startTime')" />
      <date-input v-model="endDate" :label="$t('time.endDate')" />
      <time-input v-model="endTime" :label="$t('time.endTime')" />
      <v-select
        v-model="selectedGroup"
        :items="schoolGroups"
        :label="$t('groups.parentGroup')"
      />
      <v-text-field v-model="location" :label="$t('myActivity.location')" />
      <v-btn
        class="mt-4"
        color="primary"
        large
        v-text="$t('userActions.save')"
        @click="onSubmit"
      />
    </v-col>
  </v-row>
</template>

<script>
import moment from "moment"
import { mapActions, mapState } from "vuex"
import store from "../vuex/store"
import Api from "../api"
import Utils from "../helpers/utils"
import { SERVER } from "../helpers/constants/constants"
import DateInput from "../components/DateInput"
import TimeInput from "../components/TimeInput"
import RadioGroup from "../components/RadioGroup"

export default {
  components: { DateInput, TimeInput, RadioGroup },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 999 })
    await store.dispatch("programGroup/getGroupList", {
      groupType: SERVER.programGroupTypes.standard,
      override: true,
    })
    next()
  },
  data() {
    return {
      startDate: "",
      startTime: "",
      endDate: "",
      endTime: "",
      selectedGroup: "",
      location: "",
      recurrence: "oneTime",
      recurrenceChoices: [
        {
          label: this.$t("time.oneTime"),
          value: "oneTime",
        },
        {
          label: this.$t("time.weeklyForYear"),
          value: "weekly",
        },
      ],
    }
  },
  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("event", ["createEvent", "createRecurringEvents" ]),
    async onSubmit() {
      const startTime = Utils.dateToApiString(
        moment(`${this.startDate}T${this.startTime}`)
      )
      const endTime = Utils.dateToApiString(
        moment(`${this.endDate}T${this.endTime}`)
      )
      const event = {
        startTime,
        endTime,
        schoolGroup: this.selectedGroup,
        locationsName: this.location,
      }
      try {
        if (this.recurrence === "oneTime") {
          await this.createEvent(event)
          this.showMessage(
            this.$t("success.eventCreatedAndWaitingForOrganizationApproval")
          )
          return this.$router.push({ name: "MyEvents" })
        }

        await this.createRecurringEvents({
          ...event,
          recurrence: this.recurrence,
        })
        this.showMessage(
          this.$t("success.eventsCreatedAndWaitingForOrganizationApproval")
        )
        ///// console.log(add validation), show only approved/grey + filter on consumers & others as well
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },
  computed: {
    ...mapState("programGroup", ["groupList"]),
    schoolGroups() {
      return this.groupList.map(group => ({
        value: group.slug,
        text: `${group.name} (${group.activityName})`,
      }))
    },
  },
}
</script>
