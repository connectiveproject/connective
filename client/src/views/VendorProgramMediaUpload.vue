<template>
  <div>
    <v-row no-gutters>
      <v-col cols="12" lg="7" class="mb-12 mb-lg-0">
        <div class="pb-12">
          <h1 v-text="$t('program.mediaUpload')" class="mb-5" />
          <h2 v-text="$t('program.uploadVideosAndImagesSoSchoolsCanView')" />
        </div>
        <carousel
          v-model="currentMediaIndex"
          :media-list="mediaList.length ? mediaList : mediaListPlaceholder"
        />
        <div class="text-center pt-12 relative">
          <v-btn class="mx-4" fab color="error" @click="triggerMediaDelete">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
          <v-btn
            fab
            data-testid="add-media-btn"
            class="mx-4"
            color="success"
            @click="triggerMediaUpload"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-btn
            data-testid="finish-btn"
            class="absolute-left"
            x-large
            outlined
            color="success"
            @click="
              $router.push({
                name: 'VendorDetailProgram',
                params: { programSlug },
              })
            "
            v-text="$t('userActions.finish')"
          />
        </div>
      </v-col>
      <v-col cols="12" lg="5" class="px-10">
        <sticky-note v-if="!$vuetify.breakpoint.mobile">
          <b>{{ this.$t("general.didYouKnow?") }}</b>
          <div
            class="pt-5 sticky-span"
            v-text="
              $t(
                'program.uploadingImagesAndVideosCanImproveTheProgramPopularity!'
              )
            "
          />
        </sticky-note>
      </v-col>
    </v-row>
    <modal-approve
      v-model="isApproveModalOpen"
      @approve="deleteMedia(currentMediaIndex)"
    >
      {{
        this.$t(
          "confirm.thisActionWillDeleteTheMediaYouAreCurrentlyWatching-Proceed?"
        )
      }}
    </modal-approve>
    <upload-modal v-model="isUploadModalOpen" @upload="uploadMedia" />
  </div>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import Api from "../api"
import Utils from "../helpers/utils"
import { CAROUSEL_PLACEHOLDER } from "../helpers/constants/images"
import store from "../vuex/store"
import ModalApprove from "../components/ModalApprove"
import Carousel from "../components/Carousel"
import StickyNote from "../components/StickyNote"
import UploadModal from "../components/VendorProgramMediaUploadModal"

export default {
  components: { ModalApprove, StickyNote, Carousel, UploadModal },
  async beforeRouteEnter(to, from, next) {
    const mediaList = await store.dispatch(
      "vendorProgram/getProgramMediaList",
      to.params.programSlug
    )
    next(vm => (vm.mediaList = mediaList))
  },
  props: {
    programSlug: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      currentMediaIndex: 0,
      mediaList: [],
      mediaListPlaceholder: [{ imageUrl: CAROUSEL_PLACEHOLDER }],
      isApproveModalOpen: false,
      isUploadModalOpen: false,
    }
  },
  methods: {
    ...mapActions("vendorProgram", [
      "deleteProgramMedia",
      "createProgramMedia",
      "getProgramMediaList",
    ]),
    ...mapActions("snackbar", ["showMessage"]),
    async deleteMedia(index) {
      try {
        await this.deleteProgramMedia(this.mediaList[index].slug)
        this.mediaList = await this.getProgramMediaList(this.programSlug)
        this.showMessage(this.$t("success.mediaDeletedSuccessfully"))
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
    triggerMediaUpload() {
      if (this.mediaList.length < 5) {
        return (this.isUploadModalOpen = true)
      }
      this.showMessage(this.$t("errors.uploadLimitIsFive"))
    },
    triggerMediaDelete() {
      this.isApproveModalOpen = true
    },
    uploadMedia: debounce(
      async function (mediaPayload) {
        try {
          const data = Utils.objectToFormData({
            activity: this.programSlug,
            ...mediaPayload,
          })
          await this.createProgramMedia(data)
          this.mediaList = await this.getProgramMediaList(this.programSlug)
          this.showMessage(this.$t("success.mediaUploadedSuccessfully"))
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

<style scoped>
.sticky-span {
  font-size: 22px;
}
</style>
