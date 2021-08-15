<template>
  <div>
    <v-snackbar :class="{ 'snackbar-width': $vuetify.breakpoint.mobile }" v-model="show">
      {{ text }}
      <template v-slot:action="{ attrs }">
        <v-btn dark text v-bind="attrs" color="primary" @click="show = false">
          {{ $t("userActions.close") }}
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === "snackbar/SHOW_MESSAGE") {
        this.show = true
        this.text = state.snackbar.text
      }
    })
  },
  data() {
    return {
      show: false,
      text: "",
    }
  },
}
</script>
<style scoped>
.snackbar-width::v-deep .v-snack__wrapper {
  width: 310px !important;
  min-width: 310px !important;
}
</style>
