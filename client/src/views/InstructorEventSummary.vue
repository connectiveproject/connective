<template>
  <v-card
    class="my-15 mx-auto px-16 py-10"
    max-width="800"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
  >
    <v-card-title v-text="$t('events.eventSummary')" class="px-0" />
    <v-card-subtitle v-text="event.activityName" class="px-0 pt-3 pb-10" />
    <title-to-text :title="$t('groups.groupName')" :text="event.schoolGroupName || $t('errors.unavailable')" />
    <title-to-text :title="$t('time.startTime')" :text="parseDate(event.startTime) || $t('errors.unavailable')" />
    <title-to-text :title="$t('time.endTime')" :text="parseDate(event.endTime) || $t('errors.unavailable')" />
    <title-to-text
      :title="$t('myActivity.location')"
      :text="event.locations_name || $t('errors.empty')"
    />
    <form class="form" @submit.prevent="onSubmit">
      <v-row>
        <v-col cols="12">
          <v-text-field
            :label="$t('events.summaryGeneralNotes')"
            v-model="summaryGeneralNotes"
            class="my-6"
          />
        </v-col>
        <v-col cols="12" sm="12" lg="6">
          <v-select
            :items="consumerchoices"
            :label="$t('events.attendance')"
            v-model="attendedConsumers"
            class="my-6"
            multiple
            dense
          />
        </v-col>
        <v-col cols="12" sm="12" lg="6">
          <v-select
            :items="[1,2,3,4,5,6,7,8,9,10]"
            v-model="summaryGeneralRating"
            :label="$t('events.summaryGeneralRating')"
            dense
            class="my-6"
          />
        </v-col>
        <v-col cols="12" sm="12" lg="6">
          <v-select
            :items="[1,2,3,4,5,6,7,8,9,10]"
            v-model="summaryChildrenBehavior"
            :label="$t('events.summaryChildrenBehavior')"
            dense
            class="my-6"
          />
        </v-col>
        </v-row>
        <v-btn
          dark
          large
          type="submit"
          color="purple darken-3"
          class="mx-auto mt-9 mb-6 px-8"
          elevation="3"
          v-text="$t('userActions.save')"
        />
    </form>
    <modal
      redirectComponentName="InstructorUnsummarizedEvents"
      v-show="isModalOpen"
    > {{ modalMsg }} </modal>
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import store from "../vuex/store"
import Utils from "../helpers/utils"
import TitleToText from "../components/TitleToText"
import Modal from "../components/Modal"

export default {
  components: { TitleToText, Modal },
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  async beforeRouteEnter(to, from, next) {
    const event = await store.dispatch(
      "instructorEvent/getEvent",
      to.params.slug
    )
    const consumers = await store.dispatch(
      "instructorProgramGroup/getConsumers",
      event.schoolGroup
    )
    next(vm => {
      vm.event = event
      vm.consumerchoices = consumers.map(c => ({ text: c.name, value: c.slug }))
      vm.attendedConsumers = consumers.map(c => c.slug)
    })
  },
  data() {
    return {
      event: {},
      consumerchoices: [],
      attendedConsumers: [],
      summaryGeneralNotes: "",
      summaryGeneralRating: 10,
      summaryChildrenBehavior: 10,
      modalMsg: this.$t("general.detailsSuccessfullyUpdated"),
      isModalOpen: false,
    }
  },
  methods: {
    ...mapActions("instructorEvent", ["updateEvent"]),
    parseDate: Utils.ApiStringToReadableDate,
    async onSubmit() {
      const payload = {
        consumers: this.attendedConsumers,
        summaryGeneralNotes: this.summaryGeneralNotes,
        summaryGeneralRating: this.summaryGeneralRating,
        summaryChildrenBehavior: this.summaryChildrenBehavior,
        hasSummary: true
      }
      await this.updateEvent({ slug: this.slug, payload })
      this.isModalOpen = true
    },
  },
}
</script>
