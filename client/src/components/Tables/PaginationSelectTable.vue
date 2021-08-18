<template>
  <base-pagination-table
    multi-sort
    v-bind="$props"
    :headers="tableHeaders"
    :items="items"
    :loading="loading"
    @paginate="$emit('paginate')"
  >
    <template v-slot:item.plus="{ item }">
      <v-icon
        size="20"
        class="mr-2"
        @click="toggleRowSelect(item)"
        color="green darken-2"
      >
        {{ isSelected(item) ? "mdi-check" : "mdi-plus" }}
      </v-icon>
    </template>
  </base-pagination-table>
</template>

<script>
import { mapActions } from "vuex"
import isEqual from "lodash/isEqual"
import BasePaginationTable from "./BasePaginationTable"

export default {
  components: { BasePaginationTable },
  model: { prop: "selectedRows" },
  props: {
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
    selectedRows: {
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
    ...mapActions("pagination", ["updatePagination"]),
    toggleRowSelect(item) {
      // add or remove from selected rows and emit correlating events
      if (!this.isSelected(item)) {
        this.$emit("input", [...this.selectedRows, item])
        this.$emit("select", item)
        return
      }
      this.$emit(
        "input",
        this.selectedRows.filter(row => !isEqual(row, item))
      )
      this.$emit("diselect", item)
    },
    isSelected(row) {
      // includes won't work due to re-fetch issues
      return this.selectedRows.filter(selected => isEqual(selected, row)).length
    },
  },
}
</script>
