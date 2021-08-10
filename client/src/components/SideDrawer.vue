<template>
  <v-navigation-drawer
    temporary
    right
    fixed
    :value="value"
    @input="$emit('input', $event)"
  >
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title v-text="title" />
          <v-list-item-subtitle v-text="subtitle" />
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-divider />
    <slot />
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      default: "",
    },
  },
}
</script>
