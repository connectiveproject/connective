<template>
  <div>
    <form-card
      v-model="fields"
      elevation="0"
      class="w-75 mx-auto"
      @valid="isFormValid = true"
      @invalid="isFormValid = false"
    />
    <v-btn
      class="white--text purple darken-3 mt-10 d-block mx-auto"
      :disabled="!isFormValid"
      @click="onSubmit"
      v-text="$t('userActions.save')"
    />
  </div>
</template>

<script>
import cloneDeep from "lodash/cloneDeep"
import { mapActions } from "vuex"
import Api from "../api"
import { VENDOR_PROGRAM_FIELDS } from "../helpers/constants/constants"
import FormCard from "../components/FormCard"

export default {
  components: { FormCard },
  data() {
    return {
      /////// ADD LOGO upload as well CONSOLE.log
      fields: cloneDeep(VENDOR_PROGRAM_FIELDS), ///// console.log(neccessary???)
      isFormValid: false,
    }
  },
  methods: {
    ...mapActions("vendorProgram", ["createProgram"]),
    ...mapActions("snackbar", ["showMessage"]),
    async onSubmit() {
      const payload = this.fields.reduce((accum, f) => (accum[f.name] = f.value), {})
      try {
        const program = await this.createProgram(payload)
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
