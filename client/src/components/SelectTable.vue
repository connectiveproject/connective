<template>
  <v-card class="pt-4">
    <v-text-field
      v-model="searchFilter"
      append-icon="mdi-magnify"
      :label="$t('userActions.search')"
      single-line
      hide-details
      class="search-bar px-10 mt-5 mb-8 mx-auto"
    />
    <v-data-table
      multi-sort
      :headers="tableHeaders"
      :items="items"
      :search="searchFilter"
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
    </v-data-table>
  </v-card>
</template>

<script>
import isEqual from "lodash/isEqual"
export default {
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
  },

  data() {
    return {
      searchFilter: "",
    }
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
      return this.selectedRows.filter(selected => isEqual(selected, row)).length
    },
  },
}
</script>
<style lang="scss" scoped>
.search-bar {
  max-width: 450px !important;
}
</style>
