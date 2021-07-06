<template>
  <v-row justify="center">
    <v-dialog :value="value" @input="close" width="540px">
      <v-card class="px-5">
        <v-card-title
          v-text="$t('program.mediaUpload')"
          class="py-8 justify-center"
        />
        <v-card-text>
          <v-select
            v-model="mediaType"
            :items="mediaTypeList"
            :label="$t('program.mediaType')"
          />
          <v-file-input
            append-icon="mdi-camera"
            :prepend-icon="null"
            type="file"
            accept="image/*"
            v-model="image"
            :disabled="mediaType === 'video'"
            :label="$t('program.imageUpload')"
          />
          <v-text-field
            append-icon="mdi-video"
            v-model="videoUrl"
            :disabled="mediaType === 'image'"
            :label="$t('program.youtubeVideoUrl')"
          />
        </v-card-text>
        <v-card-actions class="py-6">
          <v-btn
            large
            v-text="$t('userActions.save')"
            color="success"
            text
            @click="upload"
          />
          <v-btn large v-text="$t('userActions.close')" text @click="close" />
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      image: null,
      videoUrl: null,
      mediaType: "image",
      mediaTypeList: [
        {
          value: "image",
          text: this.$t("general.image"),
        },
        {
          value: "video",
          text: this.$t("general.video"),
        },
      ],
    }
  },
  methods: {
    close() {
      this.$emit("input", false)
    },
    upload() {
      const userInput = { mediaType: this.mediaType }
      this.mediaType === "image"
        ? (userInput.imageUrl = this.image)
        : (userInput.videoUrl = this.videoUrl)
      this.$emit("upload", userInput)
      this.$emit("input", false)
      this.image = null
      this.videoUrl = null
    },
  },
}
</script>
