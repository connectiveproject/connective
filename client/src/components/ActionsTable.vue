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
      <template v-slot:item.actions="{ item }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              introjs="actions-table-icon-one"
              size="20"
              class="mx-3"
              v-bind="attrs"
              v-on="on"
              :color="actionOneIconColor"
              @click="$emit('action-one-click', item)"
            >
              {{ actionOneIcon }}
            </v-icon>
          </template>
          <span>{{ actionOneIconTooltip }}</span>
        </v-tooltip>

        <v-tooltip bottom v-if="totalActions >= 2">
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              size="20"
              class="mx-3"
              v-bind="attrs"
              v-on="on"
              :color="actionTwoIconColor"
              @click="$emit('action-two-click', item)"
            >
              {{ actionTwoIcon }}
            </v-icon>
          </template>
          <span>{{ actionTwoIconTooltip }}</span>
        </v-tooltip>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import i18n from "../plugins/i18n"

export default {
  props: {
    actionsTitle: {
      type: String,
      default: "",
    },
    totalActions: {
      type: Number,
      default: 2
    },
    actionOneIcon: {
      type: String,
      default: "mdi-check",
    },
    actionTwoIcon: {
      type: String,
      default: "mdi-close",
    },
    actionOneIconColor: {
      type: String,
      default: "green darken-2",
    },
    actionTwoIconColor: {
      type: String,
      default: "red darken-1",
    },
    actionOneIconTooltip: {
      type: String,
      default: i18n.t("userActions.confirm"),
    },
    actionTwoIconTooltip: {
      type: String,
      default: i18n.t("userActions.deny"),
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
  },

  data() {
    return {
      searchFilter: "",
    }
  },

  computed: {
    tableHeaders() {
      return [...this.headers, { text: this.actionsTitle, value: "actions", sortable: false }]
    },
  },
}
</script>
<style lang="scss" scoped>
.search-bar {
  max-width: 450px !important;
}
</style>
