<template>
  <v-row no-gutters>
    <v-col class="secondary relative" cols="12" lg="5">
      <router-view />
    </v-col>
    <v-col class="relative d-none d-lg-block overflow-hidden" lg="7">
      <video width="800" :src="video" autoplay playsinline loop muted class="absolute-center" />
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
