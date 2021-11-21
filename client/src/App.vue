<template>
  <div id="app" :class="checkRtl() ? 'rtl' : 'ltr'">
    <v-app>
      <router-view />
      <snackbar />
    </v-app>
  </div>
</template>

<script>
import Utils from "@/helpers/utils"
import Snackbar from "@/components/Snackbar"

export default {
  components: { Snackbar },
  methods: {
    checkRtl: Utils.checkRtl,
  },
}
</script>
