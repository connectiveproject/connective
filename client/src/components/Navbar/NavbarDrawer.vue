<template>
  <v-navigation-drawer
    :value="value"
    @input="$emit('input', $event)"
    disable-resize-watcher
    disable-route-watcher
    app
    right
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

    <v-list nav dense>
      <v-list-item-group>
        <v-list-item
          v-for="item in navItems"
          :key="item.id"
          :to="{ name: item.componentName }"
          @click="$emit('input', false)"
        >
          <v-list-item-icon>
            <v-icon v-text="item.icon" color="primary" />
          </v-list-item-icon>
          <v-list-item-title> {{ item.text }} </v-list-item-title>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    navItems: {
      // [ { icon: String, text: String, componentName: String (comp to route to) }, ... ]
      type: Array,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      required: true,
    },
  },
}
</script>
