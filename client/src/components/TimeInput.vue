<template>
  <v-dialog
    ref="dialog"
    v-model="modal"
    :return-value="value"
    @update:return-value="e => $emit('input', e)"
    persistent
    width="90%"
    max-width="550px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        :value="value"
        @input="e => $emit('input', e)"
        :label="label"
        :class="textFieldClasses"
        append-icon="mdi-clock-time-four-outline"
        readonly
        v-bind="{ ...attrs, ...$attrs }"
        v-on="on"
      />
    </template>
    <v-time-picker
      v-if="modal"
      :value="value"
      @input="e => $emit('input', e)"
      color="primary"
      full-width
      format="24hr"
      :landscape="!$vuetify.breakpoint.xs"
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
import i18n from "@/plugins/i18n"

export default {
  inheritAttrs: false,
  props: {
    value: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      default: i18n.t("userActions.timeChoose"),
    },
    textFieldClasses: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      modal: false,
    }
  },
}
</script>
