<template>
  <v-card class="mx-auto" width="290" height="436">
    <v-img height="150px" :src="imgUrl">
      <v-overlay class="align-end justify-start" absolute opacity="0.25">
        <v-card-title class="white--text pr-8 pb-3" v-text="title" />
      </v-overlay>
    </v-img>
    <v-card-subtitle v-text="subtitle" class="pb-3" />
    <v-card-text v-text="trimmedBody" class="text--primary" />

    <v-card-actions class="absolute-bottom mb-1">
      <v-btn
        color="orange"
        text
        class="absolute-center"
        v-text="$tc('general.additionalInfo', 1)"
        @click="$emit('click')"
      />
      <v-icon
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
import { infoCardImage } from "../helpers/constants/images"
export default {
  props: {
    imgUrl: {
      type: String,
      required: false,
      default: infoCardImage,
    },
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      required: false,
    },
    body: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      starred: false,
    }
  },

  methods: {
    onStarClick() {
      this.starred = !this.starred
      if (this.starred) {
        this.$emit("star")
      }
      else {
        this.$emit("unstar")
      }
    }
  },

  computed: {
    trimmedBody() {
      // TODO: create filter
      if (this.body.length > 150) {
        return this.body.substring(0, 150) + "...."
      }
      return this.body
    },
  },
}
</script>
