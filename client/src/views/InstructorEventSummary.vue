<template>
  <v-card
    class="my-15 mx-auto px-16 py-10"
    max-width="800"
    :elevation="$vuetify.breakpoint.mobile ? 0 : 3"
  >
    <v-card-title v-text="$t('events.eventSummary')" class="px-0" />
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
    <form class="mt-16 form" @submit.prevent="onSubmit">
      <v-card style="background: #feece5">
        <v-row style="padding: 30px">
          <v-col>
            <img :src="CONFIDENTIAL_WATERMARK" alt="confidential" />
          </v-col>
          <v-card-text
            v-text="`${$t('posts.thisPostIsNotVisibleForStudents')}.`"
          />

          <v-col cols="12">
            <v-tribute :options="tributeOptions">
              <v-textarea
                outlined
                :label="$t('events.summaryGeneralNotes')"
                v-model="summaryGeneralNotes"
                class="my-6"
              >
              </v-textarea>
            </v-tribute>
          </v-col>
          <v-col cols="12" sm="12" lg="6">
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
          <v-col cols="12" sm="12" lg="6">
            <v-select
              outlined
              :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
              v-model="summaryGeneralRating"
              :label="$t('events.summaryGeneralRating')"
              dense
              class="my-6"
            />
          </v-col>
          <v-col cols="12" sm="12" lg="6">
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

      <v-checkbox
        class="mt-16"
        v-model="addPost"
        :label="$t('userActions.addPublicPost')"
      />
      <v-card elevation="0" v-if="addPost">
        <v-card-title class="px-0" v-text="$t('userActions.addPost')" />
        <v-card-subtitle
          class="px-0"
          v-text="`${$t('posts.thisPostWillBeVisibleForEveryone')}.`"
        />
        <v-row class="my-2">
          <v-col cols="12">
            <v-tribute :options="tributeOptions">
              <v-textarea
                outlined
                :label="$t('events.eventFeedShareContent')"
                v-model="feedContent"
                required
              >
              </v-textarea>
            </v-tribute>
          </v-col>
          <v-col>
            <v-file-input
              v-model="images"
              accept="image/*"
              outlined
              multiple
              append-icon="mdi-paperclip"
              prepend-icon=""
              :label="$t('userActions.addMedia')"
              @change="previewImage"
            >
              <template v-slot:selection="{ text }">
                <v-chip small label color="primary" v-text="text" />
              </template>
            </v-file-input>
            <v-img v-for="url in imageUrls" :key="url" :src="url" />
          </v-col>
        </v-row>
      </v-card>
      <v-btn
        large
        type="submit"
        color="primary"
        class="mx-auto mt-9 mb-6 px-8"
        elevation="3"
        v-text="$t('userActions.save')"
      />
    </form>
    <modal
      redirectComponentName="InstructorUnsummarizedEvents"
      v-show="isModalOpen"
    >
      {{ modalMsg }}
    </modal>
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Api from "../api"
import Utils from "../helpers/utils"
import { CONFIDENTIAL_WATERMARK } from "../helpers/constants/images"
import VTribute from "../components/VTribute"
import TitleToText from "../components/TitleToText"
import Modal from "../components/Modal"

export default {
  components: {
    TitleToText,
    Modal,
    VTribute,
  },
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
      event: {},
      addPost: true,
      tributeOptions: {
        trigger: "@",
        values: [],
        positionMenu: true,
        // TODO: add noMatchTemplate
        // noMatchTemplate: "<li>השם לא נמצא</li>",
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
      imageUrls: [],
      images: [],
    }
  },
  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("instructorEvent", [
      "updateEvent",
      "createFeedPost",
      "createPostImages",
    ]),
    parseDate: Utils.ApiStringToReadableDate,
    onSubmit: debounce(
      async function () {
        try {
          if (this.addPost) {
            await Promise.all([this.createSummary(), this.createPost()])
          } else {
            await this.createSummary()
          }
          this.isModalOpen = true
        } catch (err) {
          const message = Api.utils.parseResponseError(err)
          this.showMessage(message)
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
        this.images.map(image =>
          this.createPostImages(
            Utils.objectToFormData({ image_url: image, post: post.slug })
          )
        )
      )
    },
    previewImage() {
      if (!this.images.length) {
        this.imageUrls = []
      }
      this.images.map(
        image =>
          (this.imageUrls = [...this.imageUrls, URL.createObjectURL(image)])
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
      transform: scale(ץ8);
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
