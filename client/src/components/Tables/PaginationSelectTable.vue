<template>
  <base-pagination-table
    v-bind="$attrs"
    :headers="tableHeaders"
    :items="items"
    :loading="loading"
    @paginate="$emit('paginate')"
  >
    <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
      <!-- use slots directly from parent -->
      <slot :name="slot" v-bind="scope" />
    </template>
    <template v-slot:item.plus="{ item }">
      <v-icon
        size="20"
        class="mr-2"
        @click="toggleRowSelect(item)"
        color="primary darken-3"
      >
        {{ isSelected(item) ? "mdi-check" : "mdi-plus" }}
      </v-icon>
    </template>
  </base-pagination-table>
</template>

<script>
import isEqual from "lodash/isEqual"
import BasePaginationTable from "./BasePaginationTable"

export default {
  components: { BasePaginationTable },
  inheritAttrs: false,
  props: {
    // selected rows
    value: {
      type: Array,
      required: true,
    },
    headers: {
      // v-data-table headers. e.g., [ { text: 'Calories', value: 'calories' }, ... ]
      type: Array,
      required: true,
    },
    items: {
      // v-data-table items (i.e., table rows)
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    tableHeaders() {
      return [{ text: "", value: "plus", sortable: false }, ...this.headers]
    },
  },

  methods: {
    toggleRowSelect(item) {
      // add or remove from selected rows and emit correlating events
      if (!this.isSelected(item)) {
        this.$emit("input", [...this.value, item])
        this.$emit("select", item)
        return
      }
      this.$emit(
        "input",
        this.value.filter(row => !isEqual(row, item))
      )
      this.$emit("diselect", item)
    },
    isSelected(row) {
      // includes won't work due to re-fetch issues
      return this.value.filter(selected => isEqual(selected, row)).length
    },
  },
}
</script>
