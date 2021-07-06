<template>
  <div>
    <pagination-select-table
      v-if="pagination"
      v-bind="$props"
      @paginate="$emit('paginate')"
      :value="selectedRows"
      @input="e => $emit('input', e)"
    />
    <select-table
      v-else
      v-bind="$props"
      :value="selectedRows"
      @input="e => $emit('input', e)"
    />

    <chip-container :labels="getChipLabels()" icon="mdi-account-circle">{{
      $t("general.chosen")
    }}</chip-container>
  </div>
</template>

<script>
// wrapper for the select table (add rows to chips bucket)
import SelectTable from "./SelectTable"
import PaginationSelectTable from "./PaginationSelectTable"
import ChipContainer from "./ChipContainer"

export default {
  components: {
    SelectTable,
    PaginationSelectTable,
    ChipContainer,
  },
  model: {
    prop: "selectedRows",
  },
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
      required: true
    },
    pagination: {
      type: Boolean,
      default: false,
    },
    totalServerItems: {
      // received from server via count field (relevant in pagination mode only)
      type: Number,
      required: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    chipsLabelHeader: {
      // headers keys to display on chip
      type: [String, Array],
      required: true,
    },
  },
  methods: {
    getChipLabels() {
      return this.selectedRows.map(row => this.getLabel(row))
    },
    getLabel(row) {
      if (!Array.isArray(this.chipsLabelHeader)) {
        return row[this.chipsLabelHeader]
      }
      let label = ""
      for (const header of this.chipsLabelHeader) {
        label += row[header] + " "
      }
      return label
    },
  },
}
</script>

<style lang="scss" scoped>
.chips-container {
  width: 650px;
  height: 300px;
  overflow-y: auto;
}
</style>
