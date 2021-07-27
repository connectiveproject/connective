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
        >
          <div class="text-center">
            <v-dialog v-model="dialog">
              <template v-slot:activator="{ on, attrs }">
                <v-img
                  style="max-width: 50vw; max-height: 50vh"
                  v-bind="attrs"
                  v-on="on"
                  :src="image"
                />
              </template>
              <v-card>
                <v-img class="show-more-overlay" :src="image" />
              </v-card>
            </v-dialog>
          </div>
        </v-col>
        <v-col v-if="showMore" cols="6">
          <v-img max-height="150" class="w-100" :src="images[4]">
            <v-overlay absolute color="#036358" class="show-more-overlay">
              <h1>{{ additionalImages }}+</h1>
            </v-overlay>
          </v-img>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import Avatar from "./Avatar/Avatar.vue"
export default {
  components: { Avatar },

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
      dialog: false,
      showMore: this.images.length > 3,
      additionalImages: this.images.length - 3,
    }
  },
}
</script>
<style scoped>
#info-button {
  letter-spacing: 1.7px !important;
}
.show-more-overlay {
  cursor: "pointer";
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
