<template>
  <v-card class="mx-auto" max-width="500" v-bind="$attrs">
    <v-toolbar :color="color" :dark="dark">
      <v-toolbar-title v-text="title" />
      <v-spacer />
    </v-toolbar>

    <v-list two-line>
      <v-list-item-group
        :value="selected"
        @change="emitChange"
        :active-class="`${color}--text`"
        multiple
      >
        <div v-for="(item, index) in items" :key="index">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />

              <v-list-item-subtitle
                class="text--primary"
                v-text="item.headline"
              />

              <v-list-item-subtitle v-text="item.subtitle" />
            </v-list-item-content>
            <div
              color="grey lighten-2"
              class="text-caption mb-6"
              v-text="item.action"
            />
          </v-list-item>
          <v-divider v-if="index < items.length - 1" />
        </div>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
export default {
  inheritAttrs: false,
  model: {
    prop: "selected",
  },
  props: {
    selected: {
      type: Array,
      required: true,
    },
    title: {
      type: String,
      default: "",
    },
    items: {
      // array of objs, containing caption, headline, subtitle, title
      type: Array,
      required: true,
    },
    color: {
      // vuetify color pallete
      type: String,
      default: "cyan",
    },
    dark: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    emitChange(e) {
      this.$emit("input", e)
    },
  },
}
</script>
