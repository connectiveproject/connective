<template>
  <div>
    <pagination-select-table
      v-if="usePagination"
      v-bind="$attrs"
      :headers="headers"
      :items="items"
      :loading="loading"
      :value="selectedRows"
      @input="$emit('input', $event)"
      @paginate="$emit('paginate')"
    />
    <select-table
      v-else
      v-bind="{ ...$props, ...$attrs }"
      :value="selectedRows"
      @input="$emit('input', $event)"
    />
    <chip-container :labels="getChipLabels()" icon="mdi-account-circle">
      {{ $t("general.chosen") }}
    </chip-container>
  </div>
</template>

<script>
// wrapper for the select table (add rows to chips bucket)
import SelectTable from "./SelectTable"
import PaginationSelectTable from "./Tables/PaginationSelectTable"
import ChipContainer from "./ChipContainer"

export default {
  components: {
    SelectTable,
    PaginationSelectTable,
    ChipContainer,
  },
  inheritAttrs: false,
  model: {
    prop: "selectedRows",
  },
  props: {
    usePagination: {
      type: Boolean,
      default: true,
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
    selectedRows: {
      type: Array,
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
