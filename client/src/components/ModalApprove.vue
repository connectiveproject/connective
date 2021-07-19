<template>
  <v-dialog
    max-width="290"
    :value="isOpen"
    @input="handleDisapprove"
  >
    <v-card>
      <v-card-title class="text-h5" v-text="$t('general.message')" />
      <v-card-text>
        <slot>{{ this.$t("confirm.AreYouSureYouWantToDelete?") }}</slot>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          text
          color="teal darken-4"
          data-testid="modal-approve-yes"
          v-text="$t('general.yes')"
          @click="handleApprove"
        />
        <v-btn
          text
          color="teal darken-4"
          v-text="$t('general.no')"
          @click="handleDisapprove"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  model: { prop: "isOpen" },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    handleDisapprove(e) {
      this.$emit("disapprove", e)
      this.$emit("input", false)
    },
    handleApprove(e) {
      this.$emit("approve", e)
      this.$emit("input", false)
    },
  },
}
</script>
