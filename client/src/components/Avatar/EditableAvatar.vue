<template>
  <hover-button @click="isDialogOpen = true" circle :shadow="false">
    <avataaars v-bind="avataaarsOptions" />
    <form-dialog
      :title="$t('auth.profilePicture')"
      v-model="isDialogOpen"
      :inputFields="dialogOptions"
      @save="saveAvatarOptions"
    />
  </hover-button>
</template>

<script>
import Avataaars from "vuejs-avataaars"
import FormDialog from "../FormDialog"
import HoverButton from "../HoverButton"
import { getDialogOptions, defaultAvatarOptions } from "./helpers"

export default {
  components: {
    Avataaars,
    FormDialog,
    HoverButton,
  },
  model: {
    prop: "avatarOptions",
  },
  props: {
    avatarOptions: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isDialogOpen: false,
      defaultAvatarOptions,
    }
  },
  methods: {
    saveAvatarOptions(options) {
      this.$emit("input", options)
    },
  },
  computed: {
    avataaarsOptions() {
      if (Object.keys(this.avatarOptions).length) {
        return this.avatarOptions
      }
      return this.defaultAvatarOptions
    },
    dialogOptions() {
      return getDialogOptions(this.avataaarsOptions)
    },
  },
}
</script>
