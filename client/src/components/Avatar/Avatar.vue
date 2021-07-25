<template>
  <avataaars v-bind="avataaarsOptions" />
</template>

<script>
import Avataaars from "vuejs-avataaars"
import { defaultAvatarOptions } from "./helpers"

export default {
  components: { Avataaars },
  props: {
    avatarOptions: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      defaultAvatarOptions,
    }
  },
  computed: {
    avataaarsOptions() {
      if (Object.keys(this.avatarOptions).length) {
        return this.avatarOptions
      }
      return this.defaultAvatarOptions
    },
  },
}
</script>
