<template>
  <v-row>
    <v-col lg="4">
      <router-view />
    </v-col>
    <v-col lg="8">
      <video :src="video" autoplay loop :style="style" />
    </v-col>
  </v-row>
</template>
<script>
import { BACKGROUNDS } from "../helpers/constants/images"
export default {
  data() {
    return {
      video: BACKGROUNDS.welcome,
      // style: {
      //   background: `url(${BACKGROUNDS.welcome})`,
      //   "background-size": "cover",
      //   "min-height": "100vh",
      // },
    }
  },
}
</script>
