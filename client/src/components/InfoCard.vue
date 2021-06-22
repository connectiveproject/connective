<template>
  <v-card class="mx-auto" :width="width" :height="height">
    <v-img :height="imgHeight" :src="imgUrl">
      <v-overlay class="align-end justify-start" absolute opacity="0.25">
        <v-card-title class="white--text pr-8 pb-3" v-text="title" />
      </v-overlay>
    </v-img>
    <v-card-subtitle v-text="subtitle" class="pb-3" />
    <v-card-text class="text--primary">
      <!-- if slot's text overflow, consider using the trim filter on parent  -->
      <slot></slot>
    </v-card-text>

    <v-card-actions class="absolute-bottom actions">
      <v-btn
        v-if="!hideButton"
        :color="buttonColor"
        text
        class="absolute-center"
        v-text="buttonText"
        @click="$emit('click')"
      />
      <v-icon
        v-if="!hideStar"
        @click="onStarClick"
        :color="starred ? 'orange' : 'grey'"
        :class="{ 'mx-2': !$vuetify.breakpoint.mobile }"
      >
        {{ starred ? "mdi-check-bold" : "mdi-check" }}
      </v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import { INFO_CARD_IMAGE } from "../helpers/constants/images"
import i18n from "../plugins/i18n"

export default {
  model: {
    prop: "starred",
  },
  props: {
    starred: {
      type: Boolean,
      required: false,
    },
    imgUrl: {
      type: String,
      default: INFO_CARD_IMAGE,
    },
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      required: false,
    },
    height: {
      type: String,
      default: "436",
    },
    width: {
      type: String,
      default: "290",
    },
    imgHeight: {
      type: String,
      default: "150",
    },
    hideStar: {
      type: Boolean,
      default: false,
    },
    hideButton: {
      type: Boolean,
      default: false,
    },
    buttonColor: {
      type: String,
      default: "orange",
    },
    buttonText: {
      type: String,
      default: i18n.tc("general.additionalInfo", 1),
    },
  },

  methods: {
    onStarClick() {
      this.$emit("input", !this.starred)
    },
  },
}
</script>
<style scoped>
.actions {
  height: 40px;
}
</style>
