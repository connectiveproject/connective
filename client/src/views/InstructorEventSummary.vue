<template>
  <v-card
    class="my-md-15 mx-auto px-4 px-md-16 py-10"
    max-width="800"
    :elevation="$vuetify.breakpoint.xs ? 0 : 3"
  >
    <v-card-title v-text="$t('events.eventSummary')" class="px-0 pb-0" />
    <a
      target="_blank"
      class="d-block mb-4 w-fit-content"
      :class="{ 'cursor-initial': !event.activityWebsite }"
      :href="event.activityWebsite"
    >
      <v-card-subtitle v-text="event.activityName" class="px-0">
        {{ event.activityName }}
      </v-card-subtitle>
    </a>
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
    <validation-observer
      tag="form"
      class="mt-16 form"
      v-slot="{ invalid }"
      @submit.prevent="onSubmit"
    >
      <v-card introjs="confidential" style="background: #feece5">
        <v-row no-gutters justify="space-between" class="pt-16 px-2 px-sm-9 pb-5" >
          <v-col>
            <v-img :src="CONFIDENTIAL_WATERMARK" alt="confidential" />
          </v-col>
          <v-card-text
            v-text="`${$t('posts.thisPostIsNotVisibleForStudents')}.`"
          />

          <v-col cols="12">
            <v-tribute :options="tributeOptions">
              <v-textarea
                autofocus
                outlined
                v-model="summaryGeneralNotes"
                class="my-6"
                persistent-hint
                :hint="$t('events.use@toTagStudents')"
                :label="
                  $t(
                    'events.summaryGeneralNotes-unusualEventsStudentsBehaviorEtc'
                  )
                "
              >
              </v-textarea>
            </v-tribute>
          </v-col>
          <v-col cols="12" sm="12" lg="5">
            <v-select
              outlined
              :items="consumerchoices"
              :label="$t('events.attendance')"
              v-model="attendedConsumers"
              class="my-6"
              multiple
              dense
            />
          </v-col>
          <v-col cols="12" sm="12" lg="5">
            <v-select
              outlined
              :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
              v-model="summaryGeneralRating"
              :label="$t('events.summaryGeneralRating')"
              dense
              class="my-6"
            />
          </v-col>
          <v-col cols="12" sm="12" lg="5">
            <v-select
              outlined
              :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
              v-model="summaryChildrenBehavior"
              :label="$t('events.summaryChildrenBehavior')"
              dense
              class="my-6"
            />
          </v-col>
        </v-row>
      </v-card>

      <v-simple-checkbox
        class="mt-16"
        v-model="addPost"
        :label="$t('userActions.addPublicPost')"
      />
      <v-card introjs="public" elevation="0" v-if="addPost">
        <v-card-title class="px-0" v-text="$t('userActions.addPost')" />
        <v-card-subtitle
          class="px-0"
          v-text="`${$t('posts.thisPostWillBeVisibleForEveryone')}.`"
        />
        <v-row no-gutters class="my-2">
          <v-col cols="12">
            <validation-provider v-slot="{ errors }" rules="required">
              <v-tribute :options="tributeOptions">
                <v-textarea
                  outlined
                  v-model="feedContent"
                  persistent-hint
                  :hint="$t('events.use@toTagStudents')"
                  :label="$t('events.postContent')"
                  :error-messages="errors"
                >
                </v-textarea>
              </v-tribute>
            </validation-provider>
          </v-col>
          <v-col>
            <validation-provider v-slot="{ errors }" rules="size:12000">
              <v-file-input
                ref="fileInput"
                v-model="images"
                accept=".gif,.jpg,.jpeg,.png"
                outlined
                multiple
                append-icon="mdi-paperclip"
                prepend-icon=""
                persistent-hint
                :error-messages="errors"
                :hint="$t('userActions.holdCtrlKeyToUploadMultipleMediaFiles')"
                :label="$t('userActions.addImages')"
                @change="compressImages"
                @click:append="
                  $refs.fileInput.$el.querySelector('input').click()
                "
              >
                <template v-slot:selection="{ text }">
                  <v-chip small label color="primary" v-text="text" />
                </template>
              </v-file-input>
            </validation-provider>
            <v-img v-for="url in imageUrls" :key="url" :src="url" />
          </v-col>
        </v-row>
      </v-card>
      <v-card-actions class="mt-9 mb-6">
        <v-btn
          large
          type="submit"
          color="primary"
          elevation="3"
          :loading="submitting"
          :disabled="invalid"
        >
          {{ $t("userActions.save") }}
        </v-btn>
        <v-btn
          large
          class="mx-3 white--text"
          color="primary"
          outlined
          v-text="$t('userActions.back')"
          @click="$router.push({ name: 'InstructorUnsummarizedEvents' })"
        />
      </v-card-actions>
    </validation-observer>
    <modal
      redirectComponentName="InstructorUnsummarizedEvents"
      v-show="isModalOpen"
    >
      {{ modalMsg }}
    </modal>
  </v-card>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate"
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Api from "../api"
import Utils from "../helpers/utils"
import { CONFIDENTIAL_WATERMARK } from "../helpers/constants/images"
import VTribute from "../components/VTribute"
import TitleToText from "../components/TitleToText"
import Modal from "../components/Modal"
import introjsSubscribeMixin from "../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "InstructorEventSummary",
  components: {
    ValidationObserver,
    ValidationProvider,
    TitleToText,
    Modal,
    VTribute,
  },
  mixins: [introjsSubscribeMixin],
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
      vm.tributeOptions.values = consumers.map(consumer => ({
        key: consumer.name,
        value: consumer.name.replace(" ", "_"),
      }))
    })
  },
  data() {
    return {
      CONFIDENTIAL_WATERMARK,
      imgCompressionPromise: null,
      event: {},
      submitting: false,
      addPost: true,
      tributeOptions: {
        trigger: "@",
        values: [],
        positionMenu: true,
        noMatchTemplate: `<li>${this.$t("errors.nameNotFound")}</li>`,
        menuContainer: document.querySelector(".menu-container"),
      },
      consumerchoices: [],
      attendedConsumers: [],
      feedContent: "",
      summaryGeneralNotes: "",
      summaryGeneralRating: 10,
      summaryChildrenBehavior: 10,
      modalMsg: this.$t("general.detailsSuccessfullyUpdated"),
      isModalOpen: false,
      images: [],
      compressedImages: [],
    }
  },
  computed: {
    imageUrls() {
      let urls = []
      this.images.map(
        image => (urls = [...urls, URL.createObjectURL(image)])
      )
      return urls
    },
  },
  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("instructorEvent", ["updateEvent"]),
    ...mapActions("eventFeedPost", ["createFeedPost", "createPostImages"]),
    parseDate: Utils.ApiStringToReadableDate,
    compressImages() {
      this.imgCompressionPromise = Promise.all(
        this.images.map(async image => Utils.compressImageFile(image))
      )
    },
    onSubmit: debounce(
      async function () {
        try {
          this.submitting = true
          this.compressedImages = await this.imgCompressionPromise
          if (this.addPost) {
            await Promise.all([this.createSummary(), this.createPost()])
          } else {
            await this.createSummary()
          }
          this.isModalOpen = true
        } catch (err) {
          const message = Api.utils.parseResponseError(err)
          this.showMessage(message)
          this.submitting = false
        }
      },
      500,
      { leading: true, trailing: false }
    ),
    createSummary() {
      const data = {
        consumers: this.attendedConsumers,
        summaryGeneralNotes: this.summaryGeneralNotes,
        summaryGeneralRating: this.summaryGeneralRating,
        summaryChildrenBehavior: this.summaryChildrenBehavior,
        hasSummary: true,
      }
      return this.updateEvent({ slug: this.slug, data })
    },
    async createPost() {
      const feedPostData = {
        event: this.slug,
        post_content: this.feedContent,
      }
      const post = await this.createFeedPost(feedPostData)
      // TODO: send them as one payload (BE supports it)
      return Promise.all(
        this.compressedImages.map(image =>
          this.createPostImages(
            Utils.objectToFormData({ image_url: image, post: post.slug })
          )
        )
      )
    },
  },
}
</script>
<style lang="scss">
div.tribute-container > ul > li {
  -webkit-text-size-adjust: 100%;
  word-break: normal;
  tab-size: 4;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  font-family: Roboto, sans-serif;
  text-align: center !important;
  box-sizing: inherit;
  align-items: center;
  cursor: default;
  display: inline-flex;
  line-height: 20px;
  max-width: 100%;
  outline: none;
  overflow: hidden;
  padding: 0 12px;
  position: relative;
  text-decoration: none;
  transition-duration: 0.28s;
  transition-property: box-shadow, opacity;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  vertical-align: middle;
  white-space: nowrap;
  margin: 8px !important;
  border-radius: 16px;
  font-size: 14px;
  height: 32px;
  background-color: #5cbbf6 !important;
  border-color: #5cbbf6 !important;
  color: #fff;
  background: #e0e0e0;
  animation: bounce-in 0.3s;

  @keyframes bounce-in {
    0% {
      transform: scale(0.8);
    }
    50% {
      transform: scale(1.1);
    }
    100% {
      transform: scale(1);
    }
  }
}
</style>
