<template>
  <v-card>
    <pagination-actions-table
      v-bind="$attrs"
      elevation="0"
      :value="value"
      @input="$emit('input', $event)"
      @paginate="$emit('paginate')"
      @action-one-click="$emit('action-one-click', $event)"
      @action-two-click="$emit('action-two-click', $event)"
    >
      <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope">
        <slot :name="slot" v-bind="scope" />
      </template>
    </pagination-actions-table>
    <v-card-actions
      introjs="table-actions"
      class="relative grey lighten-5 mt-3"
    >
      <v-btn
        @click="onBtnOneClick"
        :class="{
          'glow-animation': !wasBtnOneClicked,
          'absolute-center': $vuetify.breakpoint.smAndUp,
        }"
        v-text="footerBtnOneText"
        :color="footerBtnOneColor"
        outlined
      />
      <v-spacer />
      <div class="pl-2">
        <v-btn
          text
          :color="footerBtnTwoColor"
          v-text="footerBtnTwoText"
          @click="$emit('footer-btn-two-click', $event)"
          :disabled="footerBtnTwoDisabled"
        />
        <v-tooltip bottom v-if="$vuetify.breakpoint.smAndUp && !hideFooterIcons">
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="triggerUpload">
              <v-icon :color="footerIconsColor">{{ footerUploadIcon }}</v-icon>
            </v-btn>
          </template>
          <span class="px-3">{{ footerUploadIconTooltip }} CSV</span>
        </v-tooltip>
        <v-tooltip bottom v-if="$vuetify.breakpoint.smAndUp && !hideFooterIcons">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
              @click="$emit('file-download-request')"
            >
              <v-icon :color="footerIconsColor">{{
                footerDownloadIcon
              }}</v-icon>
            </v-btn>
          </template>
          <span class="px-3">{{ footerDownloadIconTooltip }}</span>
        </v-tooltip>
      </div>
    </v-card-actions>
    <v-file-input
      :id="`upload-input-${_uid}`"
      class="d-none"
      type="file"
      accept=".csv"
      v-model="file"
    />
  </v-card>
</template>

<script>
import i18n from "../../plugins/i18n"
import PaginationActionsTable from "./PaginationActionsTable"

export default {
  components: { PaginationActionsTable },
  props: {
    value: {
      // selected rows. relevant only when using show-select
      type: Array,
      default: () => [],
    },
    footerBtnOneText: {
      type: String,
      default: "",
    },
    footerBtnOneColor: {
      type: String,
      default: "primary",
    },
    footerBtnTwoText: {
      type: String,
      default: "",
    },
    footerBtnTwoColor: {
      type: String,
      default: "error",
    },
    footerBtnTwoDisabled: {
      type: Boolean,
      default: false,
    },
    footerUploadIcon: {
      type: String,
      default: "mdi-file-upload",
    },
    footerUploadIconTooltip: {
      type: String,
      default: i18n.t("userActions.import"),
    },
    footerDownloadIcon: {
      type: String,
      default: "mdi-file-download-outline",
    },
    footerDownloadIconTooltip: {
      type: String,
      default: i18n.t("userActions.export"),
    },
    footerIconsColor: {
      type: String,
      default: "primary",
    },
    hideFooterIcons: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    triggerUpload() {
      document.getElementById(`upload-input-${this._uid}`).click()
    },
    onBtnOneClick(e) {
      this.$emit("footer-btn-one-click", e)
      this.wasBtnOneClicked = true
    },
  },
  data() {
    return {
      file: null,
      wasBtnOneClicked: false,
    }
  },
  watch: {
    file() {
      if (this.file) {
        this.$emit("file-upload", this.file)
        this.file = null
      }
    },
  },
}
</script>

<style></style>
