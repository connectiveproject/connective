<template>
  <div>
    <v-row v-if="!editMode || disabled" @click="edit()" cols="12">
      <v-col cols="11">
        <div v-if="contentFormat === 'richText'">
          <p v-if="value" v-html="value"></p>
          <p
            v-else
            v-html="placeholder || label"
            class="font-weight-light light"
          ></p>
        </div>
        <div v-else>
          <h3 v-if="value" v-text="value" class="font-weight-regular" />
          <h3
            v-else
            v-text="placeholder || label"
            class="font-weight-light light"
          />
        </div>
      </v-col>
      <v-col cols="1">
        <v-btn class="float-end" icon v-if="!disabled" @click="edit()">
          <v-icon>mdi-pen</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-text-field
      v-else-if="contentFormat === 'text'"
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
    <div v-else-if="contentFormat === 'richText'">
      <editor
        v-click-outside="onClickOutsideField"
        v-model="activeValue"
        :apiKey="tinyMceApiKey"
        :init="{
          height: 200,
          menubar: false,
          content_style: 'body {font-size: 12pt;}',
          plugins: [
            'advlist autolink lists link image charmap',
            'searchreplace visualblocks code fullscreen',
            'print preview anchor insertdatetime media',
            'paste code wordcount table directionality',
          ],
          toolbar:
            'undo redo | formatselect | fontsizeselect | bold italic underline strikethrough | \
        alignleft aligncenter alignright | \
        bullist numlist outdent indent | ltr rtl',
        }"
      />
      <v-btn icon @click="onSave" slot="append">
        <v-icon>mdi-content-save</v-icon>
      </v-btn>
    </div>
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
import Editor from "@tinymce/tinymce-vue"
export default {
  components: {
    ModalApprove,
    Editor,
  },
  props: {
    value: {
      // note: this value updates only on save
      type: String,
      required: true,
      default: "",
    },
    label: {
      type: String,
      required: false,
    },
    placeholder: {
      type: String,
      default: "",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    contentFormat: {
      type: String,
      default: "text",
    },
  },
  data() {
    return {
      tinyMceApiKey: process.env.VUE_APP_TINYMCE_API_KEY,
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
    edit() {
      if (!this.disabled) {
        this.activeValue = this.value
        this.editMode = true
      }
    },
  },
}
</script>
<style scoped>
.light {
  color: #d8d8d8;
}
</style>>
