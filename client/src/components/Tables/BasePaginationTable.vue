<template>
  <v-card class="pt-3" :elevation="elevation">
    <v-text-field
      v-if="!hideSearch"
      v-model="searchFilter"
      data-testid="table-searchbar"
      class="search-bar px-10 mt-5 mb-8 mx-auto"
      append-icon="mdi-magnify"
      single-line
      hide-details
      :label="$t('userActions.search')"
      @click:append="onSearch"
      @keyup.enter="onSearch"
    />

    <v-select
      v-if="filter1Field"
      v-model="filter1Value"
      class="search-bar px-10 mt-5 mb-8 mx-auto"
      @change="onSearch"
      :label="filter1Label"
      :items="filter1Items"
    />

    <v-data-table
      multi-sort
      v-bind="$attrs"
      :headers="headers"
      :items="items"
      :loading="loading"
      :loading-text="loadingText"
      :server-items-length="
        useSecondaryPagination ? totalServerItemsSecondary : totalServerItems
      "
      :value="value"
      @input="$emit('input', $event)"
      @update:options="paginate"
    >
      <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
        <slot :name="slot" v-bind="scope" />
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import { mapState } from "vuex"
import i18n from "@/plugins/i18n"

export default {
  inheritAttrs: false,
  props: {
    value: {
      // selected rows. relevant only when using show-select
      type: Array,
      default: () => [],
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
    loadingText: {
      type: String,
      default: i18n.t("general.loading"),
    },
    hideSearch: {
      type: Boolean,
      default: false,
    },
    elevation: {
      type: String,
      default: "2",
    },
    useSecondaryPagination: {
      type: Boolean,
      default: false,
    },
    filter1Label: {
      type: String,
      default: "Filter 1",
    },
    filter1Field: {
      type: String,
    },
    filter1Items: {
      type: Array,
      default: () => ["Filter Option 1", "Filter Option 2"],
    },
  },
  data() {
    return {
      searchFilter: "",
      options: {},
      filter1Value: "",
    }
  },
  methods: {
    updatePagination(options) {
      if (this.useSecondaryPagination) {
        return this.$store.dispatch("pagination2/updatePagination", options)
      }
      return this.$store.dispatch("pagination/updatePagination", options)
    },
    async paginate(options) {
      await this.updatePagination(options)
      this.$emit("paginate")
    },
    async onSearch() {
      this.options.page = 1
      let fieldFilters = {}
      if (this.filter1Field && this.filter1Value) {
        fieldFilters[this.filter1Field] = this.filter1Value
      }
      await this.updatePagination({
        searchFilter: this.searchFilter,
        fieldFilters: fieldFilters,
      })
      this.$emit("paginate")
    },
  },
  computed: {
    ...mapState("pagination", ["totalServerItems"]),
    ...mapState("pagination2", {
      totalServerItemsSecondary: "totalServerItems",
    }),
  },
}
</script>
<style lang="scss" scoped>
.search-bar {
  max-width: 450px !important;
}
</style>
