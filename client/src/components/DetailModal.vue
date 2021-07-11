<template>
  <div v-show="value">
    <v-overlay />
    <v-card v-bind="$attrs" class="px-7 py-5 fixed-center z-index-5" max-width="344">
      <v-card-text>
        <p v-text="topSubtitle" />
        <p class="text-h4 text--primary" v-text="title" />
        <p v-text="bottomSubtitle" />
        <div class="text--primary">
          <slot></slot>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          class="mx-auto"
          color="primary"
          v-text="buttonText"
          @click="close"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    value: {
      // is open
      type: Boolean,
      required: true,
    },
    topSubtitle: {
      type: [String, Number],
      default: "",
    },
    title: {
      type: [String, Number],
      required: true,
    },
    bottomSubtitle: {
      type: [String, Number],
      default: "",
    },
    buttonText: {
      type: String,
      default: "Close",
    },
  },
  methods: {
    close() {
      this.$emit("input", false)
    },
  },
}
</script>
