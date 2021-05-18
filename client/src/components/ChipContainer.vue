<template>
  <v-card class="chips-container mx-auto mt-15" elevation="5" v-bind="$attrs">
    <v-card-title><slot></slot></v-card-title>
    <v-chip-group class="chips-group" column show-arrows>
      <v-chip
        color="indigo"
        text-color="white"
        class="ma-2"
        v-for="label in labels"
        :key="label.index"
      >
        <v-avatar v-if="icon" left>
          <v-icon>{{ icon }}</v-icon>
        </v-avatar>
        {{ label }}
      </v-chip>
    </v-chip-group>
  </v-card>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    labels: {
      type: Array,
      required: true,
    },
    icon: {
      type: String,
      required: false,
    },
  },
}
</script>
