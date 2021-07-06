<template>
  <div id="app">
    <v-app>
      <router-view />
      <snackbar />
    </v-app>
  </div>
</template>

<script>
import Snackbar from "./components/Snackbar.vue"
export default {
  components: { Snackbar },
}
</script>
