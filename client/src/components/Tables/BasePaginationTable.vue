<template>
  <v-card class="pt-3" :elevation="elevation">
    <v-text-field
      v-if="!hideSearch"
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
      v-bind="$attrs"
      :headers="headers"
      :items="items"
      :loading="loading"
      :loadingText="loadingText"
      :server-items-length="totalServerItems"
      @update:options="paginate"
    >
      <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
        <slot :name="slot" v-bind="scope" />
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import i18n from "../../plugins/i18n"

export default {
  inheritAttrs: false,
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
  },
  data() {
    return {
      searchFilter: "",
      options: {},
    }
  },
  methods: {
    ...mapActions("pagination", ["updatePagination"]),
    async paginate(options) {
      await this.updatePagination(options)
      this.$emit("paginate")
    },
    async onSearch() {
      this.options.page = 1
      await this.updatePagination({ searchFilter: this.searchFilter })
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
