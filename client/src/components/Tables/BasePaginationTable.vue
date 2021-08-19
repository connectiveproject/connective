<template>
  <v-card class="pt-3" :elevation="elevation">
    <v-text-field
      v-if="!hideSearch"
      v-model="searchFilter"
      class="search-bar px-10 mt-5 mb-8 mx-auto"
      append-icon="mdi-magnify"
      single-line
      hide-details
      :label="$t('userActions.search')"
      @click:append="onSearch"
      @keyup.enter="onSearch"
    />
    <v-data-table
      multi-sort
      v-bind="$attrs"
      :headers="headers"
      :items="items"
      :loading="loading"
      :loading-text="loadingText"
      :server-items-length="totalServerItems"
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
import { mapActions, mapState } from "vuex"
import i18n from "../../plugins/i18n"

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
  computed: {
    ...mapState("pagination", ["totalServerItems"]),
  },
}
</script>
<style lang="scss" scoped>
.search-bar {
  max-width: 450px !important;
}
</style>
