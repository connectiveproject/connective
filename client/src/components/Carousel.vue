<template>
  <v-carousel
    v-bind="$attrs"
    height="350"
    class="mt-6 mx-auto rounded-lg grey darken-3"
    show-arrows-on-hover
    :hide-delimiters="hideDelimiters"
    hide-delimiter-background
    delimiter-icon="mdi-minus"
    @change="e => $emit('input', e)"
  >
    <v-carousel-item
      v-for="media in mediaList"
      :key="media.id"
      reverse-transition="fade-transition"
      transition="fade-transition"
      class="text-center"
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
      <img v-else :src="media.imageUrl" height="350" />
    </v-carousel-item>
  </v-carousel>
</template>
<script>
import Utils from "../helpers/utils"

export default {
  inheritAttrs: false,
  props: {
    mediaList: {
      // format: [ { mediaType: "image/video", videoUrl: "", imageUrl: ""} ]
      type: Array,
      required: true,
    },
    hideDelimiters: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    youtubeToEmbeddedUrl: Utils.youtubeToEmbeddedUrl,
  },
}
</script>
