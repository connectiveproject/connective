<template>
  <div>
    <div class="d-lg-flex justify-space-between">
      <div class="mx-auto">
        <h1 v-text="$t('program.programCreation')" class="mb-5" />
        <h2
          v-text="$t('program.fillInTheDetailsAndCreateNewProgram')"
          class="mb-8"
        />
        <form-card
          v-model="fields"
          elevation="0"
          class="w-lg-75 mx-auto mx-lg-0"
          @valid="isFormValid = true"
          @invalid="isFormValid = false"
        />
      </div>
      <picture-input
        v-model="logoField.value"
        persist-upload-button
        class="my-10 mx-auto align-self-center mx-lg-16"
        :placeholderPicUrl="CAMERA_ROUNDED_DRAWING"
        rules="size:5000"
      />
    </div>
    <div class="text-center text-lg-start mt-16 mb-8">
      <v-btn
        data-testid="save-btn"
        large
        v-text="$t('userActions.save')"
        class="white--text primary"
        :disabled="!isFormValid"
        @click="onSubmit"
      />
      <v-btn
        class="mx-3 white--text"
        color="primary"
        outlined
        large
        v-text="$t('userActions.back')"
        @click="$router.go(-1)"
      />
    </div>
  </div>
</template>

<script>
import cloneDeep from "lodash/cloneDeep"
import { mapActions } from "vuex"
import Api from "../api"
import Utils from "../helpers/utils"
import { VENDOR_PROGRAM_FIELDS } from "../helpers/constants/constants"
import { CAMERA_ROUNDED_DRAWING } from "../helpers/constants/images"
import FormCard from "../components/FormCard"
import PictureInput from "../components/PictureInput"

export default {
  components: { FormCard, PictureInput },
  data() {
    const fields = cloneDeep(VENDOR_PROGRAM_FIELDS)
    return {
      CAMERA_ROUNDED_DRAWING,
      fields,
      isFormValid: false,
      logoField: fields.filter(field => field.name === "logo")[0],
    }
  },
  methods: {
    ...mapActions("vendorProgram", ["createProgram"]),
    ...mapActions("snackbar", ["showMessage"]),
    async onSubmit() {
      try {
        const data = this.fields.reduce(
          (accum, f) => ({ ...accum, [f.name]: f.value }),
          { tags: [] }
        )
        data.activityWebsiteUrl = Utils.addWebsiteScheme(
          data.activityWebsiteUrl
        )
        const program = await this.createProgram(Utils.objectToFormData(data))
        this.showMessage(this.$t("success.programCreatedSuccessfully"))
        this.$router.push({
          name: "VendorProgramMediaUpload",
          params: { programSlug: program.slug },
        })
      } catch (err) {
        const message = Api.utils.parseResponseError(err)
        this.showMessage(message)
      }
    },
  },
}
</script>
