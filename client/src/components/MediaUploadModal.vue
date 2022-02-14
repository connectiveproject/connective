<template>
  <v-row justify="center">
    <v-dialog :value="value" @input="close" width="540px">
      <v-card class="px-5">
        <v-card-title
          v-text="$t('general.media')"
          class="py-8 justify-center"
        />
        <validation-observer v-slot="{ invalid }" slim>
          <v-card-text>
            <v-select
              :value="mediaType"
              @input="$emit('update:mediaType', $event)"
              data-testid="media-type-select"
              :items="mediaTypeList"
              :label="$t('program.mediaType')"
            />
            <validation-provider
              v-slot="{ errors }"
              v-show="mediaType === 'image'"
              :rules="mediaType === 'image' ? 'required|size:5000' : ''"
            >
              <v-file-input
                ref="fileInput"
                append-icon="mdi-camera"
                :prepend-icon="null"
                type="file"
                accept="image/*"
                v-model="image"
                :label="$t('program.imageUpload')"
                :error-messages="errors"
                clearable
                @click:append="$refs.fileInput.$el.querySelector('input').click()"
              />
            </validation-provider>
            <validation-provider
              v-slot="{ errors }"
              v-show="mediaType === 'video'"
              :rules="mediaType === 'video' ? 'required|youtubeUrl' : ''"
            >
              <v-text-field
                append-icon="mdi-video"
                v-model="videoUrl"
                :label="$t('program.youtubeVideoUrl')"
                :error-messages="errors"
                clearable
              />
            </validation-provider>
          </v-card-text>
          <v-card-actions class="py-6">
            <v-btn
              text
              large
              color="primary"
              v-text="$t('userActions.save')"
              :disabled="invalid"
              data-testid="save-btn"
              @click="upload"
            />
            <v-btn large v-text="$t('userActions.cancel')" color="primary" text @click="close" />
          </v-card-actions>
        </validation-observer>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate"
export default {
  components: { ValidationObserver, ValidationProvider },
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    mediaType: {
      type: String,
      validator(value) {
        return ["image", "video"].includes(value)
      }
    }
  },
  data() {
    return {
      image: null,
      videoUrl: null,
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
  watch: {
    mediaType(value) {
      if (value === "image") {
        this.videoUrl = null
        return
      }
      this.image = null
    },
  },
}
</script>
