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
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="325"
              height="58"
              viewBox="0 0 325 58"
            >
              <g fill="none" fill-rule="evenodd">
                <g>
                  <g>
                    <g>
                      <path
                        fill="#EC7442"
                        stroke="#EC7442"
                        stroke-width=".8"
                        d="M97.624 21.438c-.027-1.308-.1-2.554-.217-3.74l2.607-.003c.213 1.57.352 3.082.419 4.534-.967-.27-1.905-.535-2.81-.791zm-.6 4.495c-.263 5.148-1.342 9.017-3.208 11.499-1.873 2.49-4.086 2.968-5.61 2.929-1.554-.04-3.092-.654-4.241-1.552.864-1.218 1.294-2.773 1.233-4.547-.036-1.058-.106-4.115-.124-4.9 1.197-.48 1.932-1.539 1.932-2.805 0-1.07-.402-2.038-1.131-2.726-.753-.71-1.772-1.053-2.948-.99-2.356.124-3.564 1.716-3.716 3.239-.147 1.48.735 2.8 2.208 3.342.022.957.122 5.393.122 6.155 0 1.192.66 2.372 1.697 3.315-.343.404-.745.76-1.203 1.06-2.168 1.424-5.24 1.45-8.215.065-9.327-4.338-7.902-17.591-7.342-22.289l2.63-.002c-.018.76-.002 1.528.052 2.302l.016.229 6.069.333-.028-.3c-.003-.029-.094-1.073-.033-2.57l17.064-.017c.172 1.515.157 2.575.156 2.594l-.003.2.194.055c.91.256 1.885.533 2.92.828l1.592.453c.018 1.306-.01 2.673-.083 4.1zM83.563 38.47c-.916-.84-1.499-1.87-1.499-2.892 0-.857-.12-6.124-.125-6.348l-.005-.186-.178-.056c-1.339-.422-2.152-1.57-2.024-2.856.13-1.301 1.176-2.662 3.223-2.77.08-.005.16-.007.24-.007.926 0 1.724.293 2.32.855.624.589.968 1.423.968 2.348 0 1.116-.658 2.005-1.76 2.38l-.181.06.004.191c0 .039.088 3.877.13 5.091.055 1.636-.332 3.068-1.113 4.19zM69.632 17.725l5.016-.005c-.039 1.057-.003 1.891.025 2.318l-5.006-.275c-.04-.685-.052-1.365-.035-2.038zm22.552-.543L75.21 17.2c.163-2.637.82-6.345 3.062-8.56 1.29-1.273 2.973-1.916 5.012-1.916.34 0 .69.018 1.048.054 3.428.34 5.827 2.7 7.132 7.015.359 1.187.581 2.368.719 3.39zM74.176 5.316c2.33-2.483 5.393-3.795 8.858-3.795 3.724 0 6.78 1.22 9.081 3.628 2.529 2.647 4.104 6.676 4.712 12.029l-4.116.004c-.14-1.06-.368-2.29-.742-3.529-1.351-4.479-3.974-7.036-7.584-7.394-2.68-.266-4.86.41-6.482 2.012-2.394 2.365-3.072 6.213-3.23 8.929l-5.023.005c.22-4.711 1.836-9.023 4.526-11.89zm22.922 15.973l-1.438-.41c-.964-.274-1.877-.533-2.732-.774-.004-.379-.026-1.261-.154-2.403l4.108-.004c.115 1.139.187 2.337.216 3.59zm3.865 1.087c-.066-1.59-.22-3.25-.461-4.978l-.032-.224-3.118.003c-.617-5.5-2.242-9.649-4.858-12.386C90.091 2.275 86.908 1 83.034 1c-3.613 0-6.809 1.37-9.24 3.96-2.778 2.96-4.445 7.402-4.668 12.245l-3.113.003-.027.23c-.373 3.11-.776 7.752.025 12.12.985 5.37 3.538 9.047 7.588 10.93 3.142 1.462 6.403 1.424 8.725-.101.5-.329.94-.717 1.314-1.158 1.23.962 2.87 1.61 4.554 1.652 1.644.042 4.036-.469 6.043-3.138 1.93-2.566 3.044-6.53 3.312-11.784.07-1.38.099-2.707.085-3.977.909.257 1.852.523 2.822.793.263 7.957-1.718 14.052-5.831 17.801-3.974 3.622-9.857 4.773-16.566 3.243-3.698-.843-8.75-3.436-14.6-6.438-8.87-4.553-19.909-10.22-30.917-12.049-6.056-1.006-11.42-.78-16.397.692C10.487 27.696 5.392 31.052 1 35.996l.392.344c8.155-9.18 18.315-12.613 31.062-10.494 10.927 1.816 21.926 7.461 30.764 11.998 5.88 3.018 10.96 5.625 14.722 6.483 1.976.45 3.882.673 5.694.673 4.5 0 8.416-1.374 11.342-4.04 4.2-3.828 6.24-10.003 6.006-18.038-.48-.081-.968-.693-.02-.546z"
                        transform="translate(1.000000, -521.000000) translate(-1.000000, 486.000000) translate(0.000000, 35.000000)"
                      />
                      <path
                        stroke="#EC7442"
                        stroke-width="1.3"
                        d="M98.92 22.066c13.878 4.675 26.368 9.683 37.47 15.026 16.654 8.014 48.666 19.569 80.737 19.569 27.949 0 63.682-6.523 107.2-19.57"
                        transform="translate(1.000000, -521.000000) translate(-1.000000, 486.000000) translate(0.000000, 35.000000)"
                      />
                      <path
                        fill="#EC7442"
                        fill-rule="nonzero"
                        d="M282.454 14V5.666h2.412c.754 0 1.154.411 1.201 1.234l.005.17V14h2.61V7.196c0-.816-.132-1.479-.396-1.989s-.63-.885-1.098-1.125c-.468-.24-1.008-.36-1.62-.36h-5.706V14h2.592zm-12.892.18c1.236-.036 2.358-.171 3.366-.405s1.869-.585 2.583-1.053c.714-.468 1.254-1.083 1.62-1.845.366-.762.531-1.701.495-2.817l-.018-.594c-.036-1.152-.375-2.064-1.017-2.736-.642-.672-1.557-1.008-2.745-1.008h-5.526l.252 1.944.99 8.514zm2.268-2.304l-.668-6.21h2.486c.23 0 .436.048.616.144l.131.081c.21.15.372.357.486.621.114.264.171.582.171.954v.54c.024.504.009.954-.045 1.35-.054.396-.153.741-.297 1.035-.144.294-.342.546-.594.756-.252.21-.567.372-.945.486-.378.114-.825.195-1.341.243zM266.228 14V5.828l-.216-2.106h-2.592l.216 2.106V14h2.592zm-7.654-3.78l2.574-.45.018-1.134V5.828l-.216-2.106h-2.592l.216 2.106v4.392z"
                        transform="translate(1.000000, -521.000000) translate(-1.000000, 486.000000) translate(0.000000, 35.000000)"
                      />
                    </g>
                  </g>
                </g>
              </g>
            </svg>
          </v-col>
          <v-card-text>יוכלו לראות: מנהל.ת בי"ס, מנהל.ת העמותה</v-card-text>

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
      <v-card-title class="my-3" v-text="$t('events.eventFeedShareTitle')" />
      <v-row class="my-3">
        <v-col cols="12">
          <v-card-text>יוכלו לראות:כולם</v-card-text>
          <v-tribute :options="tributeOptions">
            <v-textarea
              outlined
              :label="$t('events.eventFeedShareContent')"
              v-model="feedContent"
              class="my-6"
              required
            >
            </v-textarea>
          </v-tribute>
        </v-col>
        <v-col>
          <v-file-input
            @change="previewImage"
            v-model="images"
            accept="image/*"
            outlined
            multiple
            prepend-icon="mdi-paperclip"
          >
            <template v-slot:selection="{ text }">
              <v-chip small label color="primary">
                {{ text }}
              </v-chip>
            </template>
          </v-file-input>
          <v-img v-for="url in imageUrls" :key="url" :src="url"></v-img>
        </v-col>
      </v-row>
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
import VTribute from "../components/VTribute"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Utils from "../helpers/utils"
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
      event: {},
      tributeOptions: {
        trigger: "@",
        values: [],
        positionMenu: true,
        // TODO: add noMatchTemplate
        noMatchTemplate: "<li>השם לא נמצא</li>",
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
    ...mapActions("instructorEvent", [
      "updateEvent",
      "createFeedPost",
      "createPostImages",
    ]),
    parseDate: Utils.ApiStringToReadableDate,
    onSubmit: debounce(
      async function () {
        await Promise.all([this.createSummary(), this.createPost()])
        this.isModalOpen = true
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
