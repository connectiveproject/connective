<template>
  <v-row
    class="pa-5 pa-sm-10 pa-md-16"
    justify="space-around"
    align="center"
    no-gutters
  >
    <v-col sm="11" lg="6" :class="{ 'pr-16': !$vuetify.breakpoint.xs }">
      <h1 class="pb-8" v-text="$t('events.eventsCreation')" />
      <validation-observer
        tag="form"
        v-slot="{ invalid }"
        @submit.prevent="onSubmit"
        :class="{ 'w-85': !$vuetify.breakpoint.xs }"
      >
        <radio-group
          class="pa-0 mb-8"
          v-model="recurrence"
          :hint="
            $t(
              'events.byChoosingWeeklyReccurenceEventsWillBeCreatedInAFixedDayForAYearBasedOnDateAndTimeSpecifiedForFirstEvent'
            )
          "
          persistent-hint
          :title="`${$t('time.recurrence')}:`"
          :choices="recurrenceChoices"
        />

        <v-switch
          v-model="permanentGroup"
          class="text-capitalize"
          :label="$t('events.permanentGroup')"
        ></v-switch>

        <validation-provider
          v-if="permanentGroup"
          v-slot="{ errors }"
          rules="required"
        >
          <v-select
            v-model="selectedGroup"
            class="mb-3"
            :items="schoolGroups"
            :label="$t('groups.parentGroup')"
            :error-messages="errors"
            v-if="permanentGroup"
          />
        </validation-provider>
        <!-- Grade  -->
        <validation-provider
          v-if="!permanentGroup"
          v-slot="{ errors }"
          rules="required"
        >
          <v-row cols="12">
            <v-col cols="2"> {{ $t("general.grade") }}: </v-col>
            <v-col cols="10">
              <v-row class="mt-2">
                <!-- button to select all grades -->
                <v-checkbox
                  v-if="!$vuetify.breakpoint.xs"
                  color="primary"
                  @change="selectAllGrades($event)"
                  :label="$t('general.all')"
                  class="me-6"
                />
                <v-checkbox
                  v-model="filterGrades"
                  v-for="(grade, index) in GRADE_CHOICES"
                  :key="grade.value"
                  :data-testid="grade.value"
                  :label="grade.text"
                  :value="grade.value"
                  :error-messages="errors"
                  :rules="gradeRequired"
                  :hide-details="index !== GRADE_CHOICES.length - 1"
                ></v-checkbox>
              </v-row>
            </v-col>
          </v-row>
        </validation-provider>
        <!-- Gender -->
        <validation-provider
          v-if="!permanentGroup"
          v-slot="{ errors }"
          rules="required"
        >
          <v-row cols="12">
            <v-col cols="2"> {{ $t("gender.gender") }}: </v-col>
            <v-col cols="10">
              <v-row class="mt-2">
                <v-checkbox
                  v-if="!$vuetify.breakpoint.xs"
                  color="primary"
                  @change="selectAllGenders($event)"
                  :label="$t('general.all')"
                  class="me-6"
                />
                <v-checkbox
                  v-model="filterGenders"
                  v-for="(grade, index) in GENDER_CHOICES"
                  :key="grade.value"
                  :data-testid="grade.value"
                  :label="grade.text"
                  :value="grade.value"
                  :error-messages="errors"
                  :rules="genderRequired"
                  :hide-details="index !== GENDER_CHOICES.length - 1"
                ></v-checkbox>
              </v-row>
            </v-col>
          </v-row>
        </validation-provider>
        <!-- Title -->
        <validation-provider
          v-if="!permanentGroup"
          v-slot="{ errors }"
          rules="required"
        >
          <v-text-field
            v-model="title"
            class="mb-3"
            :label="$t('events.title')"
            :error-messages="errors"
          />
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          rules="required"
          name="eventDate"
        >
          <date-input
            v-model="eventDate"
            text-field-classes="mb-3"
            :label="$t('time.eventDate')"
            :error-messages="errors"
          />
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          rules="required"
          name="startTime"
        >
          <time-input
            v-model="startTime"
            text-field-classes="mb-3"
            :label="$t('time.eventStartTime')"
            :error-messages="errors"
          />
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          rules="required|afterStartTime:@startTime"
        >
          <time-input
            v-model="endTime"
            text-field-classes="mb-3"
            :label="$t('time.eventEndTime')"
            :error-messages="errors"
          />
        </validation-provider>

        <validation-provider
          v-if="!permanentGroup"
          v-slot="{ errors }"
          rules="required"
        >
          <v-select
            :disabled="permanentGroup"
            v-model="selectedInstructor"
            class="mb-3"
            :items="availableInstructorsOptions"
            :label="$t('general.instructor')"
            :error-messages="errors"
          />
        </validation-provider>
        <v-autocomplete
          chips
          deletable-chips
          multiple
          small-chips
          :items="availableInstructorsOptions"
          v-model="additionalStaff"
          :label="$t('events.additionalStaff')"
          :no-data-text="$t('events.noInstructorsFound')"
        />
        <validation-provider v-slot="{ errors }" rules="required">
          <v-text-field
            v-model="location"
            class="mb-3"
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
        <v-btn
          class="mt-4 mx-4"
          color="primary"
          outlined
          large
          v-text="$t('userActions.back')"
          @click="$router.go(-1)"
        />
      </validation-observer>
    </v-col>
    <v-col sm="11" lg="6" v-if="!$vuetify.breakpoint.xs">
      <v-img style="border-radius: 10px" :src="img" />
    </v-col>
  </v-row>
</template>

<script>
import moment from "moment"
import { mapActions, mapState } from "vuex"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import store from "@/vuex/store"
import Api from "@/api"
import Utils from "@/helpers/utils"
import { SERVER } from "@/helpers/constants/constants"
import { CREATE_EVENT } from "@/helpers/constants/images"
import { GRADE_CHOICES, GENDER_CHOICES } from "@/views/ConsumerList/constants"
import DateInput from "@/components/DateInput"
import TimeInput from "@/components/TimeInput"
import RadioGroup from "@/components/RadioGroup"

export default {
  components: {
    DateInput,
    TimeInput,
    RadioGroup,
    ValidationObserver,
    ValidationProvider,
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 500 })
    await store.dispatch("programGroup/getGroupList", {
      groupType: [
        SERVER.programGroupTypes.standard,
        SERVER.programGroupTypes.noRegistration,
      ],
      override: true,
      usePagination: true,
    })
    next()
  },
  async created() {
    const instructorsApiRes = await Api.organization.getInstructorList({
      // TODO
    })
    this.availableInstrcutorsForGroup = instructorsApiRes.data["results"]
  },
  props: {
    groupSlug: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      img: CREATE_EVENT,
      eventDate: "",
      startTime: "12:00",
      endTime: "12:00",
      availableInstrcutorsForGroup: [],
      selectedGroup: this.groupSlug,
      title: "",
      selectedInstructor: null,
      instructorName: "",
      additionalStaff: [],
      location: "",
      recurrence: SERVER.eventOrderReccurence.oneTime,
      GRADE_CHOICES,
      GENDER_CHOICES,
      recurrenceChoices: [
        {
          label: this.$t("time.oneTime"),
          value: SERVER.eventOrderReccurence.oneTime,
        },
        {
          label: this.$t("time.weeklyFor52Weeks"),
          value: SERVER.eventOrderReccurence.weekly,
        },
      ],
      permanentGroup: true,
      filterGrades: [],
      filterGenders: [],
    }
  },
  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("event", ["createEventOrder"]),
    async onSubmit() {
      const startTime = Utils.dateToApiString(
        moment(`${this.eventDate}T${this.startTime}`)
      )
      const endTime = Utils.dateToApiString(
        moment(`${this.eventDate}T${this.endTime}`)
      )
      await this.submitEventOrder(startTime, endTime)
    },
    async submitEventOrder(startTime, endTime) {
      let eventOrder = {
        startTime,
        endTime,
        locationsName: this.location,
        recurrence: this.recurrence,
        additionalInstructors: this.additionalStaff,
      }
      if (this.permanentGroup) {
        eventOrder["schoolGroup"] = this.selectedGroup
      } else {
        eventOrder["filterGrades"] = this.filterGrades
        eventOrder["filterGenders"] = this.filterGenders
        eventOrder["title"] = this.title
        eventOrder["instructor"] = this.selectedInstructor
      }
      try {
        eventOrder = await this.createEventOrder(eventOrder)
        if (eventOrder.status === SERVER.eventOrderStatus.approved) {
          // event order was approved automatically --> event created
          this.showMessage(this.$t("success.eventSuccessfullyCreated"))
          return this.$router.go(-1)
        } else {
          // event order is pending approval
          this.showMessage(
            this.$t("success.orderCreatedAndWaitingForOrganizationApproval")
          )
          return this.$router.push({ name: "CoordinatorEventOrderStatus" })
        }
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
    selectAllGrades(checked) {
      if (checked) {
        this.filterGrades = this.GRADE_CHOICES.map(grade => grade.value)
      } else {
        this.filterGrades = []
      }
    },
    selectAllGenders(checked) {
      if (checked) {
        this.filterGenders = this.GENDER_CHOICES.map(gender => gender.value)
      } else {
        this.filterGenders = []
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
    availableInstructorsOptions() {
      return this.availableInstrcutorsForGroup.map(instructor => ({
        value: instructor.slug,
        text: instructor.name,
      }))
    },
    gradeRequired() {
      return [this.filterGrades.length > 0 || this.$t("validation.required")]
    },
    genderRequired() {
      return [this.filterGenders.length > 0 || this.$t("validation.required")]
    },
  },
}
</script>
