<template>
  <side-drawer
    v-bind="$attrs"
    :title="title"
    :subtitle="subtitle"
    :value="value"
    @input="$emit('input', $event)"
  >
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
  </side-drawer>
</template>

<script>
import SideDrawer from "./SideDrawer"

export default {
  inheritAttrs: false,
  components: { SideDrawer },
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
      default: "",
    },
  },
}
</script>
