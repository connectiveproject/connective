<template>
  <v-container fluid>
    <p>{{ title }}</p>
    <v-radio-group :value="selectedItem" @change="onChange">
      <v-radio
        v-for="choice in choices"
        :key="choice.id"
        :label="choice.label"
        :value="choice.value"
      />
    </v-radio-group>
  </v-container>
</template>
<script>
export default {
  model: {
    prop: "selectedItem",
  },
  props: {
    selectedItem: {
      // empty string or item a value from choices prop
      type: String,
      required: true,
    },
    choices: {
      type: Array,
      required: true,
      validator(value) {
        return value.every(
          item =>
            Object.keys(item).includes("label") &&
            Object.keys(item).includes("value")
        )
      },
    },
    title: {
      type: String,
      required: true,
    },
  },
  methods: {
    onChange(e) {
      this.$emit("input", e)
    },
  },
}
</script>
