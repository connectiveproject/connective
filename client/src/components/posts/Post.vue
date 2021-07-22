<template>
  <div :width="width" class="my-3">
    <v-card
      class="mx-auto card overflow-hidden"
      elevation="1"
      :width="width"
      :height="height"
    >
      <v-row>
        <v-col md="auto" class="ms-3 pe-0">
          <v-list-item-avatar color="grey darken-3">
            <v-img class="elevation-6" alt="" :src="authorIcon"></v-img>
          </v-list-item-avatar>
        </v-col>
        <v-col md="auto" class="px-0">
          <v-card-title v-text="author" class="pa-2 font-weight-bold" />
        </v-col>
      </v-row>
      <v-row class="my-0 p-0">
        <v-col md="auto" class="ms-3 pe-0">
          <v-card-subtitle
            v-text="subtitle"
            class="px-2 pt-2 pb-1 subtitle-1"
          />
        </v-col>
      </v-row>
      <v-card-text class="text--primary pt-3 px-2 subtitle-1 body">
        <!-- if slot's text overflow, consider using the trim filter on parent  -->
        <slot>{{ content }}</slot>
      </v-card-text>
      <v-row class="my-3">
        <v-col md="auto" v-for="image in images.slice(0, 3)" :key="image.url">
          <div class="text-center">
            <v-dialog v-model="dialog" width="500">
              <template v-slot:activator="{ on, attrs }">
                <v-img
                  v-bind="attrs"
                  v-on="on"
                  class="showMoreOverlay"
                  max-height="150"
                  alt=""
                  :src="image.url"
                ></v-img>
              </template>

              <v-card>
                <v-img class="showMoreOverlay" alt="" :src="image.url"></v-img>
              </v-card>
            </v-dialog>
          </div>
        </v-col>
        <v-col md="auto" v-if="showMore">
          <v-img max-height="150" alt="" :src="images[6].url"
            ><v-overlay absolute color="#036358" class="showMoreOverlay">
              <h1>{{ additionalImages }}+</h1>
            </v-overlay></v-img
          >
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
export default {
  components: {},

  props: {
    width: {
      type: String,
      default: "600",
    },
    content: {
      type: String,
      default:
        "place holder place holder place ",
    },
    author: {
      type: String,
      default: "place holder",
    },
    subtitle: {
      type: Date,
      default: new Date(),
    },
    authorIcon: {
      type: String,
      default:
        "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light",
    },
    images: {
      type: Array,
      default: () => [
        {
          url: "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light",
        },
      ],
    },
  },

  methods: {
    toggleModal: function () {
      alert("11111")
    },
  },
  data() {
    return {
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
.showMoreOverlay {
  cursor: "pointer";
}
.actions {
  height: 40px;
}
.card {
  border-radius: 4px;
}
.body {
  line-height: 1.4;
}
</style>
