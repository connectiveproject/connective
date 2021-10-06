<template>
  <v-card
    class="mx-auto card overflow-hidden"
    elevation="1"
    :width="width"
    :height="height"
  >
    <v-card-title v-text="title" class="pa-2 font-weight-bold" />
    <v-card-subtitle class="px-2 pt-2 pb-1 subtitle-1">
      <slot name="subtitle"></slot>
    </v-card-subtitle>
    <v-img
      :height="imgHeight"
      :src="imgUrl"
      @click="imgClickable && $emit('click')"
      :class="{ 'cursor-pointer': imgClickable }"
    />
    <v-card-text class="text--primary pt-3 px-2 subtitle-1 body">
      <!-- if slot's text overflow, consider using the trim filter on parent  -->
      <slot></slot>
    </v-card-text>
    <v-card-actions class="absolute-bottom actions justify-center">
      <v-btn
        text
        id="primary-button"
        data-testid="info-btn"
        v-if="!hideButton"
        :color="buttonColor"
        class="subtitle-1 font-weight-bold"
        v-text="buttonText"
        @click="$emit('click')"
      />
      <v-btn
        text
        id="secondary-button"
        v-if="secondaryButtonText"
        @click="$emit('secondary-click')"
        class="subtitle-1 font-weight-bold"
        :class="{ 'mx-2': !$vuetify.breakpoint.xs }"
        :color="secondaryButtonColor"
        v-text="secondaryButtonText"
      />
    </v-card-actions>
  </v-card>
</template>

<script>
import { INFO_CARD_IMAGE } from "../helpers/constants/images"
import i18n from "@/plugins/i18n"

export default {
  props: {
    imgUrl: {
      type: String,
      default: INFO_CARD_IMAGE,
    },
    imgClickable: {
      type: Boolean,
      default: true,
    },
    title: {
      type: String,
      required: true,
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
    hideButton: {
      type: Boolean,
      default: false,
    },
    buttonColor: {
      type: String,
      default: "orange",
    },
    secondaryButtonColor: {
      type: String,
      default: "orange",
    },
    buttonText: {
      type: String,
      default: i18n.tc("general.additionalInfo", 1),
    },
    secondaryButtonText: {
      type: String,
      default: "",
    },
  },
}
</script>
<style scoped>
#primary-button,
#secondary-button {
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
