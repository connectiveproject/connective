<template>
  <div id="app">
    <v-app>
      <router-view />
      <snackbar />
    </v-app>
  </div>
</template>

<script>
import Snackbar from "@/components/Snackbar"
import { onIdle } from "@/plugins/idleVue"

export default {
  components: { Snackbar },
  onIdle,
}
</script>
