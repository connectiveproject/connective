<template>
  <div class="wrapper mt-15 mx-auto px-3">
    <h1 class="mb-5">{{ $tc("general.schoolDetails", 0) }}</h1>
    <h2 class="pb-12">{{ $t("general.pleaseFillAllDetailsBelow") }}</h2>
    <validation-observer v-slot="{ invalid }">
      <form @submit.prevent="submitSchoolDetails">
        <v-row>
          <v-col class="pb-10" cols="12" sm="12" lg="8">
            <input-drawer
              v-for="field in textFields"
              :key="field.id"
              v-model="field.value"
              :uniqueName="field.uniqueName"
              :label="field.label"
              :rules="field.rules"
              :choices="field.choices || []"
              :type="field.type || 'text'"
            />
          </v-col>
          <v-col cols="12" sm="12" lg="3">
            <picture-input
              class="mx-auto"
              :placeholderPicUrl="placeholderPicUrl"
              @fileUpload="setPicture"
            />
          </v-col>
        </v-row>
        <v-btn
          class="my-16 white--text mx-auto mx-sm-0 d-block"
          type="submit"
          color="primary"
          elevation="3"
          :disabled="invalid"
        >
          {{ $t("userActions.save") }}
        </v-btn>
      </form>
    </validation-observer>
    <modal v-show="popupMsg !== ''" @close="popupMsg = ''">
      {{ popupMsg }}
    </modal>
  </div>
</template>
<script>
import { ValidationObserver } from "vee-validate"
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../vuex/store"
import Modal from "../components/Modal"
import InputDrawer from "../components/InputDrawer"
import PictureInput from "../components/PictureInput"
import {
  SCHOOL_GRADES_ITEMS,
  ZIP_CODE_VALIDATION_RULE,
} from "../helpers/constants/constants"
import { HOUSE_ROUNDED_DRAWING } from "../helpers/constants/images"

export default {
  components: {
    ValidationObserver,
    Modal,
    InputDrawer,
    PictureInput,
  },

  async beforeRouteEnter(to, from, next) {
    try {
      let schoolDetails = await store.dispatch("school/getSchoolDetails")
      next(vm => vm.setSchoolAttributes(schoolDetails))
    } catch (err) {
      next(vm => (vm.popupMsg = vm.$t("errors.genericError")))
    }
  },

  data() {
    return {
      textFields: {
        name: {
          uniqueName: "name",
          label: this.$t("general.name"),
          rules: "required",
          value: "",
        },
        city: {
          uniqueName: "city",
          label: this.$t("general.city"),
          rules: "required",
          value: "",
        },
        street: {
          uniqueName: "street",
          label: this.$t("general.street"),
          rules: "required",
          value: "",
        },
        zipCode: {
          uniqueName: "zipCode",
          label: this.$t("general.zipCode"),
          rules: ZIP_CODE_VALIDATION_RULE,
          value: "",
        },
        schoolCode: {
          uniqueName: "schoolCode",
          label: this.$t("general.schoolCode"),
          rules: "required|numeric",
          value: "",
        },
        description: {
          uniqueName: "description",
          label: this.$t("general.description"),
          rules: "",
          value: "",
        },
        contactPhone: {
          uniqueName: "contactPhone",
          label: this.$t("general.phoneNumber"),
          rules: "required|numeric|phoneNumberIsrael",
          value: "",
        },
        website: {
          uniqueName: "website",
          label: this.$t("general.website"),
          rules: "website",
          value: "",
        },
        grades: {
          uniqueName: "grades",
          label: this.$t("general.schoolGrades"),
          rules: "required",
          value: [],
          type: "select",
          choices: SCHOOL_GRADES_ITEMS,
        },
      },
      placeholderPicUrl: HOUSE_ROUNDED_DRAWING,
      profilePicFile: null,
      popupMsg: "",
    }
  },

  methods: {
    ...mapActions("school", ["updateSchoolDetails"]),
    setSchoolAttributes(schoolAttributes) {
      // set school profile data received from server
      this.textFields.name.value =
        schoolAttributes.name || this.textFields.name.value
      this.textFields.city.value =
        schoolAttributes.addressCity || this.textFields.city.value
      this.textFields.street.value =
        schoolAttributes.address || this.textFields.street.value
      this.textFields.zipCode.value =
        schoolAttributes.zipCity || this.textFields.zipCode.value
      this.textFields.schoolCode.value =
        schoolAttributes.schoolCode || this.textFields.schoolCode.value
      this.textFields.contactPhone.value =
        schoolAttributes.contactPhone || this.textFields.contactPhone.value
      this.textFields.description.value =
        schoolAttributes.description || this.textFields.description.value
      this.textFields.website.value =
        schoolAttributes.website || this.textFields.website.value
      this.textFields.grades.value =
        schoolAttributes.gradeLevels || this.textFields.grades.value
      this.placeholderPicUrl =
        schoolAttributes.profilePicture || this.placeholderPicUrl
      this.schoolSlug = schoolAttributes.slug
    },

    submitSchoolDetails: debounce(
      function () {
        let schoolDataPayload = this.createSchoolSubmitPayload()
        this.postSchoolData(schoolDataPayload)
      },
      500,
      { leading: true, trailing: false }
    ),

    createSchoolSubmitPayload() {
      let data = new FormData()
      data.append("slug", this.schoolSlug)
      data.append("name", this.textFields.name.value)
      data.append("address", this.textFields.street.value)
      data.append("address_city", this.textFields.city.value)
      data.append("zip_city", this.textFields.zipCode.value)
      data.append("school_code", this.textFields.schoolCode.value)
      data.append("description", this.textFields.description.value)
      data.append("contact_phone", this.textFields.contactPhone.value)
      data.append("website", this.textFields.website.value)
      data.append("grade_levels", JSON.stringify(this.textFields.grades.value))
      if (this.profilePicFile) {
        data.append("profilePicture", this.profilePicFile)
      }
      return data
    },

    async postSchoolData(schoolPayload) {
      try {
        await this.updateSchoolDetails({
          slug: this.schoolSlug,
          schoolDetails: schoolPayload,
        })
        this.popupMsg = this.$t("general.detailsSuccessfullyUpdated")
      } catch (err) {
        if (
          err.response.status === 400 &&
          Object.keys(err.response.data).length > 0
        ) {
          this.popupMsg =
            err.response.data[Object.keys(err.response.data)[0]][0]
        } else {
          this.popupMsg = this.$t("errors.genericError")
        }
      }
    },

    setPicture(file) {
      this.profilePicFile = file
    },
  },
}
</script>
<style lang="scss" scoped>
.wrapper {
  width: 90%;
}
</style>
