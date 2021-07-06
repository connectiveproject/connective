<template>
  <v-tabs color="grey darken-4" class="pb-10">
    <v-tab
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
  },
}
</script>
