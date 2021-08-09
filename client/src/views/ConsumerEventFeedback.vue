<template>
  <v-card
    class="my-15 mx-auto px-16 py-10"
    max-width="800"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
  >
    <v-card-title v-text="$t('events.eventFeedback')" class="px-0" />
    <v-card-subtitle v-text="event.activityName" class="px-0 pt-3 pb-10" />
    <title-to-text
      :title="$t('groups.groupName')"
      :text="event.schoolGroupName || $t('errors.unavailable')"
    />
    <title-to-text
      :title="$t('time.startTime')"
      :text="parseDate(event.startTime) || $t('errors.unavailable')"
    />
    <title-to-text
      :title="$t('time.endTime')"
      :text="parseDate(event.endTime) || $t('errors.unavailable')"
    />
    <title-to-text
      :title="$t('myActivity.location')"
      :text="event.locationsName || $t('errors.empty')"
    />
    <form-card
      focus
      elevation="0"
      v-model="form"
      @valid="isFormValid = true"
      @invalid="isFormValid = false"
    />
    <v-btn
      large
      color="primary"
      class="mx-auto mt-9 mb-6 px-8"
      elevation="3"
      v-text="$t('userActions.save')"
      @click="onSubmit"
      :disabled="!isFormValid"
    />
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Api from "../api"
import Utils from "../helpers/utils"
import TitleToText from "../components/TitleToText"
import FormCard from "../components/FormCard"

export default {
  components: { TitleToText, FormCard },
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  async beforeRouteEnter(to, from, next) {
    const event = await store.dispatch("consumerEvent/getEvent", to.params.slug)
    next(vm => (vm.event = event))
  },
  data() {
    return {
      isFormValid: false,
      event: {},
      form: [
        {
          name: "generalNotes",
          rules: "required|max:400",
          label: this.$t(
            "events.summarizeYourExperienceInTheEventAndWriteWhatYouLearned"
          ),
          value: "",
        },
        {
          name: "secondaryNotes",
          rules: "required|max:400",
          label: this.$t("events.writeProsAndCons"),
          value: "",
        },
        {
          name: "generalRating",
          rules: "required",
          label: this.$t("events.chooseYourLevelOfSatisfactionFromTheEvent"),
          type: "select",
          choices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
          value: "",
        },
        {
          name: "secondaryRating",
          rules: "required",
          type: "select",
          choices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
          label: this.$t(
            "events.chooseHowLikelyYouAreToRecommendThisActivityToAFriend"
          ),
          value: "",
        },
      ],
    }
  },
  methods: {
    ...mapActions("consumerEvent", ["createEventFeedback"]),
    ...mapActions("snackbar", ["showMessage"]),
    parseDate: Utils.ApiStringToReadableDate,
    onSubmit: debounce(
      async function () {
        try {
          const feedback = this.form.reduce(
            (accum, field) => ({ ...accum, [field.name]: field.value }),
            { event: this.slug }
          )
          await this.createEventFeedback(feedback)
          this.showMessage(this.$t("general.detailsSuccessfullyUpdated"))
          this.$router.push({ name: "ConsumerPendingEventsFeedback" })
        } catch (err) {
          this.showMessage(Api.utils.parseResponseError(err))
        }
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
