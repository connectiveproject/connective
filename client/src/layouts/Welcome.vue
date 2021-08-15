<template>
  <v-row no-gutters>
    <v-col class="px-2 secondary relative" cols="12" lg="5">
      <router-view />
    </v-col>
    <v-col class="relative d-none d-lg-block overflow-hidden" lg="7">
      <video
        width="800"
        class="absolute-center"
        autoplay
        playsinline
        loop
        muted
        :src="video"
      />
    </v-col>
  </v-row>
</template>
<script>
import { BACKGROUNDS } from "../helpers/constants/images"
export default {
  data() {
    return {
      video: BACKGROUNDS.welcome,
    }
  },
}
</script>
