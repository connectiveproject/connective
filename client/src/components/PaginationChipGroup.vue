<template>
  <v-chip-group
    multiple
    column
    color="primary"
    text-color="white"
    v-model="selectedChipsNumeric"
    class="mx-auto"
    @change="chipFilterChange"
  >
    <v-chip
      filter
      v-for="chip in chips"
      :key="chip"
      active-class="primary--text"
      class="filter-chip"
    >
      {{ chip }}
    </v-chip>
  </v-chip-group>
</template>
<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"

export default {
  props: {
    chips: {
      // e.g., [ "opt1", "opt2", ... ]
      type: Array,
      required: true,
    },
  },
  methods: {
    ...mapActions("pagination", ["addFieldFilter", "removeFieldFilter"]),
    chipFilterChange: debounce(async function() {
      if (this.selectedChipsNumeric.length) {
        const chipsSelected = this.selectedChipsNumeric.map(chip => this.chips[chip])
        await this.addFieldFilter({ fieldName: "chips", value: chipsSelected })
      } else {
        await this.removeFieldFilter("chips")
      }
    }, 500),
  },
  data() {
    return {
      selectedChipsNumeric: [],
    }
  },
}
</script>
<style scoped>
.filter-chip {
  margin: 5px;
}
</style>
