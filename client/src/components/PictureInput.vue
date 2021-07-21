<template>
  <v-hover v-slot="{ hover }">
    <div class="w-fit-content">
      <v-avatar size="260">
        <validation-provider
          slim
          v-slot="{ errors }"
          name="picUpload"
          rules="size:5000"
        >
          <v-file-input
            :id="inputId"
            class="d-none"
            type="file"
            accept="image/*"
            v-model="picFile"
          >
          </v-file-input>
          <div
            v-if="errors[0]"
            class="error-msg red--text text-center font-weight-bold"
          >
            {{ errors[0] }}
          </div>
        </validation-provider>
        <v-btn
          @click="triggerPicUpload()"
          v-show="hover"
          color="blue-grey"
          class="pic-btn ma-2 white--text"
          fab
        >
          <v-icon dark>mdi-cloud-upload</v-icon>
        </v-btn>
        <img :src="picSource" />
      </v-avatar>
    </div>
  </v-hover>
</template>
<script>
import { ValidationProvider } from "vee-validate"
import Utils from "../helpers/utils"
import { JPG_DOCUMENT } from "../helpers/constants/images"

export default {
  components: {
    ValidationProvider,
  },

  props: {
    placeholderPicUrl: {
      type: String,
      required: false,
      default: JPG_DOCUMENT,
    },
  },

  data() {
    return {
      picFile: undefined,
      inputId: `${this._uid}_picUpload`,
    }
  },

  methods: {
    triggerPicUpload() {
      document.getElementById(this.inputId).click()
    },
  },

  watch: {
    picFile: function () {
      this.$emit("fileUpload", this.picFile)
    },
  },

  computed: {
    picSource() {
      if (this.picFile) {
        return Utils.uploadedFileToUrl(this.picFile)
      } else {
        return this.placeholderPicUrl
      }
    },
  },
}
</script>
<style lang="scss" scoped>
$dark-strong: rgba(0, 0, 0, 0.75);
$dark-light: rgba(0, 0, 0, 0.2);

.pic-btn {
  z-index: 2;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -webkit-box-shadow: 0px 0px 26px 200px $dark-light;
  -moz-box-shadow: 0px 0px 26px 200px $dark-light;
  box-shadow: 0px 0px 26px 200px $dark-light;
}

.error-msg {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 80%;
  transform: translate(-50%, -50%);
  background-color: $dark-strong;
  -webkit-box-shadow: 0px 0px 26px 200px $dark-strong;
  -moz-box-shadow: 0px 0px 26px 200px $dark-strong;
  box-shadow: 0px 0px 26px 200px $dark-strong;
}
</style>
