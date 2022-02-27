<template>
  <div>
    <v-row v-if="!editMode">
      <v-col>
        <h3 v-text="value || label" class="font-weight-regular" />
      </v-col>
      <v-col>
        <v-btn class="float-end" icon @click="editMode = true">
          <v-icon>mdi-pen</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-text-field
      v-else
      v-click-outside="onClickOutsideField"
      v-model="activeValue"
      class="mt-5"
      :label="label"
    >
      <v-btn icon @click="onSave" slot="append">
        <v-icon>mdi-content-save</v-icon>
      </v-btn>
    </v-text-field>
    <modal-approve
      v-model="isUnsavedChangesModalOpen"
      @approve="onSave"
      @disapprove="onDiscard"
    >
      {{
        this.$t(
          "confirm.someDetailsWereEditedButNotSaved-WouldYouLikeToSaveThem?"
        )
      }}
    </modal-approve>
  </div>
</template>

<script>
import ModalApprove from "@/components/ModalApprove"

export default {
  components: {
    ModalApprove,
  },
  props: {
    value: {
      // note: this value updates only on save
      type: String,
    },
    label: {
      type: String,
    },
  },
  data() {
    return {
      editMode: false,
      isUnsavedChangesModalOpen: false,
      activeValue: this.value,
    }
  },
  methods: {
    onClickOutsideField() {
      if (this.value !== this.activeValue) {
        console.log(this.value, this.activeValue)
        this.isUnsavedChangesModalOpen = true
      } else {
        this.editMode = false
      }
    },
    onSave() {
      this.editMode = false
      this.$emit("input", this.activeValue)
    },
    onDiscard() {
      this.editMode = false

      this.activeValue = this.value
    },
  },
}
</script>
