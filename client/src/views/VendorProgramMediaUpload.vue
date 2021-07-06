<template>
  <v-row no-gutters>
    <v-col cols="12" lg="7" class="mb-12 mb-lg-0">
      <div>
        <h1 v-text="$t('program.mediaUpload')" class="mb-5" />
        <h2
          v-text="$t('program.uploadVideosAndImagesSoSchoolsCanView')"
          class=""
        />
      </div>
      <v-file-input
        v-for="i in 3" :key="i"
        accept="image/*"
        prepend-icon="mdi-folder-multiple-image"
        label="Images and Videos"
        :disabled="imageList.length >= i"
      />
    </v-col>
    <v-col cols="12" lg="5" class="px-10">
      <sticky-note>
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

  <!-- <v-card class="mt-8 pt-5 px-12 pb-14" max-width="650">
    <v-card-title>upload images & videos</v-card-title>
    <v-file-input
      accept="image/*"
      prepend-icon="mdi-camera"
      label="Logo"
    />
    <v-file-input
      accept="image/png, image/jpeg, image/bmp"
      prepend-icon="mdi-folder-multiple-image"
      label="Images and Videos"
      multiple
    >
      <template v-slot:selection="{ text }">
        <v-chip v-text="text" />
      </template>
    </v-file-input>
    <v-btn
      class="d-block mt-8 mx-auto white--text"
      type="submit"
      color="purple darken-3"
      elevation="3"
      v-text="$t('userActions.save')"
      :disabled="invalid"
    />
  </v-card> -->
</template>

<script>
import { mapActions } from "vuex"
import StickyNote from "../components/StickyNote"
import store from "../vuex/store"
export default {
  components: { StickyNote },
  async beforeRouteEnter(to, from, next) {
    const mediaList = await store.dispatch(
      "vendorProgram/getProgramMediaList",
      to.params.programSlug
    )
    console.log(mediaList)
    next(vm => (vm.mediaList = mediaList))
  },
  props: {
    programSlug: {
      type: String,
      required: true,
    },
  },
  mounted() {
    // classify images & videos
    for (const media of this.mediaList) {
      if (media.mediaType === "video") {
        this.videoList.push(media.videoUrl)
      } else {
        this.imageList.push(media.imageUrl)
      }
    }
  },
  data() {
    return {
      mediaList: null,
      videoList: [],
      imageList: [],
    }
  },
  methods: {
    ...mapActions("vendorProgram", [
      "deleteProgramMedia",
      "createProgramMedia",
    ]),
  },
}
</script>

<style scoped>
.sticky-span {
  font-size: 22px;
}
</style>
