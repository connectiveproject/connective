<template>
  <base-pagination-table
    multi-sort
    v-bind="{ ...$props, ...$attrs }"
    :headers="tableHeaders"
    :items="items"
    :no-data-text="noDataText"
    :loading="loading"
    :value="value"
    @input="$emit('input', $event)"
    @paginate="$emit('paginate')"
  >
    <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
      <slot :name="slot" v-bind="scope" />
    </template>
    <template v-slot:item.actions="{ item }">
      <div class="d-flex">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              data-testid="actions-table-action-one"
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
              data-testid="actions-table-action-two"
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
      </div>
    </template>
  </base-pagination-table>
</template>

<script>
import i18n from "@/plugins/i18n"
import BasePaginationTable from "./BasePaginationTable"

export default {
  inheritAttrs: false,
  components: { BasePaginationTable },
  props: {
    value: {
      // selected rows. relevant only when using show-select
      type: Array,
      default: () => [],
    },
    noDataText: {
      type: String,
      required: false,
    },
    actionsTitle: {
      type: String,
      default: "",
    },
    totalActions: {
      type: Number,
      default: 2,
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
    actionsFirst: {
      // align actions as the first column
      type: Boolean,
      default: false,
    },

    /* pagination table related */
    headers: {
      type: Array,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    tableHeaders() {
      if (this.actionsFirst) {
        return [
          { text: this.actionsTitle, value: "actions", sortable: false },
          ...this.headers,
        ]
      }
      return [
        ...this.headers,
        { text: this.actionsTitle, value: "actions", sortable: false },
      ]
    },
  },
}
</script>
