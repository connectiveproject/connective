<template>
  <v-card class="mx-auto card overflow-hidden" elevation="1" :width="width" :height="height">
    <v-card-title v-text="title" class="pa-2 font-weight-bold" />
    <v-card-subtitle
      v-text="subtitle"
      class="px-2 pt-2 pb-1 subtitle-1"
    />
    <v-img :height="imgHeight" :src="imgUrl" />
    <v-card-text class="text--primary pt-3 px-2 subtitle-1 body">
      <!-- if slot's text overflow, consider using the trim filter on parent  -->
      <slot></slot>
    </v-card-text>
    <v-card-actions class="absolute-bottom actions">
      <v-btn
        text
        id="info-button"
        data-testid="info-btn"
        v-if="!hideButton"
        :color="buttonColor"
        class="subtitle-1 font-weight-bold absolute-center"
        v-text="buttonText"
        @click="$emit('click')"
      />
      <v-icon
        v-if="!hideStar"
        @click="onStarClick"
        :color="value ? buttonColor : 'grey'"
        :class="{ 'mx-2': !$vuetify.breakpoint.mobile }"
      >
        {{ value ? "mdi-check-bold" : "mdi-check" }}
      </v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
import { INFO_CARD_IMAGE } from "../helpers/constants/images"
import i18n from "../plugins/i18n"

export default {
  props: {
    // whether starred or not
    value: {
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
      default: "382",
    },
    width: {
      type: String,
      default: "272",
    },
    imgHeight: {
      type: String,
      default: "195",
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
      this.$emit("input", !this.value)
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
}
.body {
  line-height: 1.4;
}
</style>
