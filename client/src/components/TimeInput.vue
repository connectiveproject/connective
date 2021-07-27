<template>
  <v-dialog
    ref="dialog"
    v-model="modal"
    :return-value.sync="value"
    persistent
    width="90%"
    max-width="550px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        :value="value"
        @input="e => $emit('input', value)"
        :label="label"
        append-icon="mdi-clock-time-four-outline"
        readonly
        v-bind="attrs"
        v-on="on"
      />
    </template>
    <v-time-picker
      v-if="modal"
      :value="value"
      @input="e => $emit('input', value)"
      color="primary"
      full-width
      format="24hr"
      landscape
      scrollable
    >
      <v-spacer />
      <v-btn
        text
        color="primary"
        @click="modal = false"
        v-text="$t('userActions.cancel')"
      />
      <v-btn
        text
        color="primary"
        @click="$refs.dialog.save(value)"
        v-text="$t('userActions.confirm')"
      />
    </v-time-picker>
  </v-dialog>
</template>
<script>
import i18n from "../plugins/i18n"

export default {
  props: {
    value: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      default: i18n.t("userActions.timeChoose"),
    },
  },
  data() {
    return {
      modal: false,
    }
  },
}
</script>
