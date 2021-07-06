<template>
  <div>
    <v-snackbar v-model="show">
      {{ text }}
      <template v-slot:action="{ attrs }">
        <v-btn dark text v-bind="attrs" color="cyan" @click="show = false">
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
