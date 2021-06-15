<template>
  <v-row justify="center">
    <v-dialog v-if="program" :value="value" @input="close" width="540px">
      <v-card class="px-5">
        <v-card-title v-text="program.name" class="py-8 justify-center" />
        <v-card-text>
          <title-to-text
            :text="program.organization"
            :title="$t('program.organization')"
          />
          <title-to-text
            :text="program.targetAudience.join(', ')"
            :title="$t('program.targetAudience')"
          />
          <title-to-text
            :text="program.description"
            :title="$t('program.description')"
          />
          <title-to-text
            v-if="!$route.meta.isConsumer"
            :text="program.contactName"
            :title="$t('program.contactName')"
          />
          <title-to-text
            v-if="!$route.meta.isConsumer"
            :text="program.phoneNumber"
            :title="$t('program.contactPhone')"
          />
          <title-to-text
            v-if="!$route.meta.isConsumer"
            :text="program.domain"
            :title="$t('program.domain')"
          />
        </v-card-text>
        <v-carousel
          v-if="mediaList.length"
          height="350"
          class="carousel mt-6 mx-auto rounded-lg"
          show-arrows-on-hover
          hide-delimiter-background
          delimiter-icon="mdi-minus"
        >
          <v-carousel-item
            v-for="media in mediaList"
            :key="media.id"
            reverse-transition="fade-transition"
            transition="fade-transition"
          >
            <iframe
              v-if="media.mediaType === 'video'"
              class="w-100"
              height="350"
              :src="youtubeToEmbeddedUrl(media.videoUrl)"
              frameborder="0"
              allow="autoplay; encrypted-media"
              allowfullscreen
            />
            <img v-else :src="media.imageUrl" class="w-100" height="350" />
          </v-carousel-item>
        </v-carousel>
        <v-card-actions class="py-6">
          <v-btn
            large
            class="mx-auto"
            v-text="$t('userActions.close')"
            color="orange"
            text
            @click="close"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import Utils from "../helpers/utils"
import TitleToText from "../components/TitleToText"

export default {
  components: { TitleToText },
  props: {
    value: {
      // indicates whether dialog is open or not
      type: Boolean,
      required: true,
    },
    program: {
      type: Object,
      required: true,
    },
    mediaList: {
      type: Array,
      required: true,
    },
  },
  methods: {
    youtubeToEmbeddedUrl: Utils.youtubeToEmbeddedUrl,
    close() {
      this.$emit("input", false)
    },
  },
}
</script>

<style lang="scss" scoped>
.carousel {
  width: 85%;
}
</style>
