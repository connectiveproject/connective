<template>
  <v-card class="mx-auto" width="290" height="436">
    <v-img height="150px" :src="imgUrl">
      <v-overlay class="align-end justify-start" absolute opacity="0.25">
        <v-card-title class="white--text pr-8 pb-3" v-text="title" />
      </v-overlay>
    </v-img>
    <v-card-subtitle v-text="subtitle" class="pb-3" />
    <v-card-text class="text--primary">
      <!-- if slot's text overflow, consider using the trim filter on parent  -->
      <slot></slot>
    </v-card-text>

    <v-card-actions class="absolute-bottom mb-1">
      <v-btn
        color="orange"
        text
        class="absolute-center"
        v-text="$tc('general.additionalInfo', 1)"
        @click="$emit('click')"
      />
      <v-icon
        v-if="showStar"
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
export default {
  model: {
    prop: "starred",
  },
  props: {
    showStar: {
      type: Boolean,
      default: true,
    },
    starred: {
      // use with showStar true
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
  },

  methods: {
    onStarClick() {
      this.$emit("input", !this.starred)
    },
  },
}
</script>
