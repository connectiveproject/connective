<template>
  <v-container fluid class="overline">
    <h3 v-text="title" class="pb-7" />
    <v-row class="justify-start">
      <v-col cols="12" md="6" v-for="item in items" :key="item.id">
        <v-checkbox
          v-model="selected"
          :label="item.label"
          :value="item.value"
          class="text-right my-n2"
        ></v-checkbox>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"

export default {
  props: {
    name: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
  },
  methods: {
    ...mapActions("pagination", ["addFieldFilter", "removeFieldFilter"]),
  },
  data() {
    return {
      selected: [],
    }
  },
  watch: {
    selected: {
      // update pagination filter
      deep: true,
      handler: debounce(function (value) {
        if (value.length) {
          this.addFieldFilter({ fieldName: this.name, value })
        } else {
          this.removeFieldFilter(this.name)
        }
      }, 500),
    },
  },
}
</script>
