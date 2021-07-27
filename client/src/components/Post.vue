<template>
  <div class="my-3" :width="width">
    <v-card
      class="card overflow-hidden w-100 pt-5 pb-10 mx-auto px-7"
      elevation="10"
    >
      <div class="d-flex justify-space-between">
        <v-card-title v-text="author" class="font-weight-bold pa-2" />
        <avatar style="width: 50px" :avatar-options="authorAvatar" />
      </div>
      <v-card-subtitle v-text="subtitle" class="px-2 py-1" />
      <v-card-text class="text--primary pt-3 px-2 text-h6 body">
        "<slot>{{ content }}</slot
        >"
      </v-card-text>
      <v-row class="my-10" justify="center" no-gutters>
        <v-col
          v-for="image in images.slice(0, 3)"
          :key="image.id"
          cols="6"
          class="pa-1"
        >
          <v-img
            class="cursor-pointer"
            @click="showCarousel = true"
            height="200"
            width="300"
            :src="image"
          />
        </v-col>
        <v-col v-if="showMore" cols="6" class="pa-1">
          <v-img
            class="cursor-pointer"
            @click="showCarousel = true"
            height="200"
            width="300"
            :src="images[3]"
          >
            <v-overlay absolute color="#036358">
              <h1>{{ additionalImages }}+</h1>
            </v-overlay>
          </v-img>
        </v-col>
      </v-row>
    </v-card>
    <v-dialog v-model="showCarousel" max-width="650">
      <carousel :media-list="carouselMedia" />
    </v-dialog>
  </div>
</template>

<script>
import Avatar from "./Avatar/Avatar"
import Carousel from "./Carousel"

export default {
  components: { Avatar, Carousel },
  props: {
    width: {
      type: String,
      default: "100%",
    },
    content: {
      type: String,
      required: true,
    },
    author: {
      type: String,
      required: true,
    },
    authorAvatar: {
      type: Object,
      required: true,
    },
    subtitle: {
      type: String,
      required: true,
    },
    images: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      showCarousel: false,
      showMore: this.images.length > 3,
      additionalImages: this.images.length - 3,
    }
  },
  computed: {
    carouselMedia() {
      return this.images.map(image => ({
        mediaType: "image",
        imageUrl: image,
      }))
    },
  },
}
</script>
<style scoped>
#info-button {
  letter-spacing: 1.7px !important;
}
.actions {
  height: 40px;
}
.card {
  border-radius: 4px;
  min-height: 285px;
}
.body {
  line-height: 1.4;
}
</style>
