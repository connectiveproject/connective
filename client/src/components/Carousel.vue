<template>
  <v-carousel
    height="350"
    class="mt-6 mx-auto rounded-lg"
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
</template>

<script>
import Utils from "../helpers/utils"

export default {
  props: {
    mediaList: {
      // format: [ { mediaType: "image/video", videoUrl: "", imageUrl: ""} ]
      type: Array,
      required: true,
    },
  },
  methods: {
    youtubeToEmbeddedUrl: Utils.youtubeToEmbeddedUrl,
  },
}
</script>
