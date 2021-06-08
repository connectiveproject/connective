<template>
  <div>
    <pagination-select-table
      v-bind="$props"
      @paginate="$emit('paginate')"
      @change="onRowsSelectionChange"
    />
    <chip-container :labels="getChipLabels()" icon="mdi-account-circle">{{
      $t("general.chosen")
    }}</chip-container>
  </div>
</template>

<script>
// wrapper for the select table (add rows to chips bucket)
import PaginationSelectTable from "./PaginationSelectTable"
import ChipContainer from "./ChipContainer"

export default {
  components: {
    PaginationSelectTable,
    ChipContainer,
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
    totalServerItems: {
      // received from server via count field
      type: Number,
      required: true,
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
  data: () => ({ selectedRows: [] }),
  methods: {
    onRowsSelectionChange(rows) {
      this.selectedRows = rows
      this.$emit("change", this.selectedRows)
    },
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
