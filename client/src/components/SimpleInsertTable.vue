<template>
  <v-card class="w-75 mx-auto pt-16">
    <v-data-table
      show-select
      multi-sort
      v-model="selectedRows"
      :headers="headers"
      :items="value"
      :items-per-page="5"
      :loadingText="loadingText"
      :itemsPerPage="-1"
      :item-key="itemKey"
    >
      <template v-slot:item.actions="{ item }">
        <!-- edit row column ("pencil") -->
        <v-icon size="20" class="mr-2" @click="editRow(item)">
          mdi-pencil
        </v-icon>
      </template>
    </v-data-table>
    <v-card-actions class="relative grey lighten-5 mt-3">
      <v-btn
        @click="openDialog()"
        :class="{ 'absolute-center': $vuetify.breakpoint.smAndUp }"
        text
        v-text="$tc('userActions.add', 1)"
      />
      <v-spacer></v-spacer>
      <div class="pl-2">
        <v-btn
          text
          color="error"
          @click="deleteRows(selectedRows)"
          :disabled="!selectedRows.length"
          v-text="$tc('userActions.remove', 2)"
        />
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon color="purple darken-4">mdi-file-upload</v-icon>
            </v-btn>
          </template>
          <span class="px-3">{{ $t("userActions.import") }} CSV</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon color="purple darken-4">mdi-file-download-outline</v-icon>
            </v-btn>
          </template>
          <span class="px-3">{{ $t("userActions.export") }}</span>
        </v-tooltip>
      </div>
    </v-card-actions>
    <form-dialog
      v-model="isDialogActive"
      :inputFields="formFields"
      @save="saveRow"
    />
    <modal v-show="popupMsg !== ''" @close="popupMsg = ''">
      {{ popupMsg }}
    </modal>
  </v-card>
</template>

<script>
import FormDialog from "./FormDialog"
import Modal from "./Modal"
import _ from "lodash"

export default {
  components: { FormDialog, Modal },
  props: {
    value: {
      // the table rows
      // empty Array, or: [ { col1: value, col2: value2, ... }, { col1: value, col2: value, ... }, ... ]
      type: Array,
      required: true,
    },
    columns: {
      // [{ name: 'column name', rule: 'validation rules for input', label: 'readable column name' }, { ... }]
      type: Array,
      required: true,
      validator(cols) {
        // heuristic validation (on first column only)
        const keys = Object.keys(cols[0])
        keys.sort()
        return _.isEqual(keys, ["label", "name", "rule"])
      },
    },
    itemKey: {
      // v-data-table item-key (column name to act as key)
      type: String,
      required: true,
    },
  },

  created() {
    // validate "value" prop based on column prop (check heuristically for missing fields)
    if (!this.$props.value.length) {
      return
    }
    const columnNames = this.$props.columns.map(col => col.name)
    const firstRow = this.$props.value[0]
    for (const field of Object.keys(firstRow)) {
      if (!columnNames.includes(field)) {
        throw `Prop Validation: '${field}' of prop 'value' does not exist in prop 'columns'`
      }
    }
  },

  data() {
    return {
      editedRowIndex: -1,
      formFields: _.cloneDeep(this.columns),
      isDialogActive: false,
      csvFile: null,
      selectedRows: [],
      loadingText: this.$t("general.loading"),
      headers: this.initHeaders(this.columns),
      popupMsg: "",
    }
  },

  methods: {
    initHeaders(columns) {
      // return a headers object for v-data-table based on the columns prop
      const headers = [{ text: "", value: "actions", sortable: false }]
      for (const col of columns) {
        headers.push({ text: col.label, value: col.name })
      }
      return headers
    },
    editRow(row) {
      this.editedRowIndex = this.value.indexOf(row)
      this.openDialog(row)
    },
    saveRow(formResult) {
      if (this.editedRowIndex > -1) {
        // edit mode - modify row
        const rows = [...this.value]
        rows[this.editedRowIndex] = formResult
        this.$emit("input", rows)
        this.editedRowIndex = -1
      } else {
        // create new row
        if (
          this.value.filter(
            row => row[this.itemKey] === formResult[this.itemKey]
          ).length
        ) {
          this.popupMsg = `${this.$t(
            "errors.recordWithTheSameValueAlreadyExists"
          )}: ${formResult[this.itemKey]}`
        } else {
          this.$emit("input", [...this.value, formResult])
        }
      }
    },
    deleteRows(selectedRows) {
      const remainingRows = this.value.filter(
        row => !selectedRows.includes(row)
      )
      this.$emit("input", remainingRows)
    },
    openDialog(rowToEdit = {}) {
      // add placeholder/default values to pass to form dialog (empty on new row, actual data on edit)
      // open dialog
      // :Object rowToEdit: { fieldName: value, ... } e.g.,  { city: 'Tel Aviv', ... }
      for (const field of this.formFields) {
        this.$set(field, "value", rowToEdit[field.name] || "")
      }
      this.isDialogActive = true
    },
  },
}
</script>
