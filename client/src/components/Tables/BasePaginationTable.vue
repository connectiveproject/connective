<template>
  <div>
    <v-text-field
      v-model="searchFilter"
      append-icon="mdi-magnify"
      :label="$t('userActions.search')"
      single-line
      hide-details
      class="search-bar px-10 mt-5 mb-8 mx-auto"
      @click:append="onSearch"
      @keyup.enter="onSearch"
    />
    <v-data-table
      multi-sort
      @update:options="paginate"
      :headers="headers"
      :items="items"
      :loading="loading"
      :loadingText="loadingText"
      :server-items-length="totalServerItems"
    />
  </div>
</template>

<script>
import { mapActions } from "vuex"
import i18n from "../../plugins/i18n"

export default {
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
    totalServerItems: {
      // received from server via count field
      type: Number,
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
  },
  data() {
    return {
      searchFilter: "",
      options: {},
    }
  },
  methods: {
    ...mapActions("pagination", ["updatePagination"]),
    paginate(options) {
      this.updatePagination(options)
      this.$emit("paginate")
    },
    onSearch() {
      this.options.page = 1
      this.updatePagination({ searchFilter: this.searchFilter })
      this.$emit("paginate")
    },
  },
}
</script>
<style lang="scss" scoped>
.search-bar {
  max-width: 450px !important;
}
</style>
