<template>
  <div>
    <v-row v-if="!editMode">
      <v-col>
        <h3 v-if="value" v-text="value" class="font-weight-regular" />
        <h3 v-else v-text="placeholder || label" class="font-weight-light" />
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
      :placeholder="placeholder"
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
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      default: "",
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
