<template>
  <v-row class="pa-16" justify="space-around" align="center" no-gutters>
    <v-col sm="11" lg="6" :class="{ 'pr-16': !$vuetify.breakpoint.mobile }">
      <h1 class="pb-8" v-text="$t('events.eventsCreation')" />
      <validation-observer
        tag="form"
        v-slot="{ invalid }"
        @submit.prevent="onSubmit"
        :class="{ 'w-75': !$vuetify.breakpoint.mobile }"
      >
        <radio-group
          class="pa-0"
          v-model="recurrence"
          :title="`${$t('time.recurrence')}:`"
          :choices="recurrenceChoices"
          row
        />
        <validation-provider v-slot="{ errors }" rules="required" name="startDate">
          <date-input
            v-model="startDate"
            :label="$t('time.startDate')"
            :error-messages="errors"
          />
        </validation-provider>
        <validation-provider v-slot="{ errors }" rules="required" name="startTime">
          <time-input
            v-model="startTime"
            :label="$t('time.startTime')"
            :error-messages="errors"
          />
        </validation-provider>
        <validation-provider v-slot="{ errors }" rules="required" name="endDate">
          <date-input
            v-model="endDate"
            :label="$t('time.endDate')"
            :error-messages="errors"
          />
        </validation-provider>

        <validation-provider v-slot="{ errors }" rules="required|afterStartDate:@startDate,@startTime,@endDate">
          <time-input
            v-model="endTime"
            :label="$t('time.endTime')"
            :error-messages="errors"
          />
        </validation-provider>
        <validation-provider v-slot="{ errors }" rules="required">
          <v-select
            v-model="selectedGroup"
            :items="schoolGroups"
            :label="$t('groups.parentGroup')"
            :error-messages="errors"
          />
        </validation-provider>
        <validation-provider v-slot="{ errors }" rules="required">
          <v-text-field
            v-model="location"
            :label="$t('myActivity.location')"
            append-icon="mdi-map-marker"
            :error-messages="errors"
          />
        </validation-provider>
        <v-btn
          type="submit"
          class="mt-4"
          color="primary"
          large
          v-text="$t('userActions.save')"
          :disabled="invalid"
        />
      </validation-observer>
    </v-col>
    <v-col sm="11" lg="6" v-if="!$vuetify.breakpoint.mobile">
      <v-img style="border-radius: 10px" :src="img" />
    </v-col>
  </v-row>
</template>

<script>
import moment from "moment"
import { mapActions, mapState } from "vuex"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import store from "../vuex/store"
import Api from "../api"
import Utils from "../helpers/utils"
import { SERVER } from "../helpers/constants/constants"
import { CREATE_EVENT } from "../helpers/constants/images"
import DateInput from "../components/DateInput"
import TimeInput from "../components/TimeInput"
import RadioGroup from "../components/RadioGroup"
export default {
  components: {
    DateInput,
    TimeInput,
    RadioGroup,
    ValidationObserver,
    ValidationProvider,
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("programGroup/getGroupList", {
      groupType: SERVER.programGroupTypes.standard,
      override: true,
    })
    next()
  },
  data() {
    return {
      img: CREATE_EVENT,
      startDate: "",
      startTime: "",
      endDate: "",
      endTime: "",
      selectedGroup: "",
      location: "",
      recurrence: SERVER.eventOrderReccurence.oneTime,
      recurrenceChoices: [
        {
          label: this.$t("time.oneTime"),
          value: SERVER.eventOrderReccurence.oneTime,
        },
        {
          label: this.$t("time.weeklyForYear"),
          value: SERVER.eventOrderReccurence.weekly,
        },
      ],
    }
  },
  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("event", ["createEventOrder"]),
    async onSubmit() {
      const startTime = Utils.dateToApiString(
        moment(`${this.startDate}T${this.startTime}`)
      )
      const endTime = Utils.dateToApiString(
        moment(`${this.endDate}T${this.endTime}`)
      )
      const eventOrder = {
        startTime,
        endTime,
        schoolGroup: this.selectedGroup,
        locationsName: this.location,
        recurrence: this.recurrence,
      }
      try {
        await this.createEventOrder(eventOrder)
        this.showMessage(
          this.$t("success.orderCreatedAndWaitingForOrganizationApproval")
        )
        return this.$router.push({ name: "CoordinatorEventOrderStatus" })
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