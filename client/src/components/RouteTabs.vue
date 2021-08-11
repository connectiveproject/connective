<template>
  <v-tabs :color="color" class="pb-10">
    <v-tab
      introjs="navigation"
      v-for="tab in tabs"
      :key="tab.id"
      :to="{ name: tab.componentName }"
      v-text="tab.text"
    />
  </v-tabs>
</template>

<script>
export default {
  props: {
    tabs: {
      // [ { componentName: "", text: "" }, ... ]
      type: Array,
      required: true,
    },
    color: {
      type: String,
      default: "grey darken-4"
    }
  },
}
</script>
