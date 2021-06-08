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
              :descriptiveName="field.descriptiveName"
              :validationRules="field.validationRules"
              :selectItems="field.selectItems || []"
              :inputType="field.inputType || 'text'"
            ></input-drawer>
          </v-col>
          <v-col cols="12" sm="12" lg="3">
            <picture-input
              class="mx-auto"
              :placeholderPicUrl="placeholderPicUrl"
              @fileUpload="setPicture"
            ></picture-input>
          </v-col>
        </v-row>
        <v-btn
          class="my-16 py-5 white--text"
          type="submit"
          color="purple darken-3"
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
import store from "../vuex/store"
import { mapActions } from "vuex"
import Modal from "../components/Modal"
import InputDrawer from "../components/InputDrawer"
import PictureInput from "../components/PictureInput"
import { SCHOOL_GRADES_ITEMS } from "../helpers/constants/constants"
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
          descriptiveName: this.$t("general.name"),
          validationRules: "required",
          value: "",
        },
        city: {
          uniqueName: "city",
          descriptiveName: this.$t("general.city"),
          validationRules: "required",
          value: "",
        },
        street: {
          uniqueName: "street",
          descriptiveName: this.$t("general.street"),
          validationRules: "required",
          value: "",
        },
        zipCode: {
          uniqueName: "zipCode",
          descriptiveName: this.$t("general.zipCode"),
          validationRules: "required|numeric",
          value: "",
        },
        schoolCode: {
          uniqueName: "schoolCode",
          descriptiveName: this.$t("general.schoolCode"),
          validationRules: "required|numeric",
          value: "",
        },
        description: {
          uniqueName: "description",
          descriptiveName: this.$t("general.description"),
          validationRules: "",
          value: "",
        },
        contactPhone: {
          uniqueName: "contactPhone",
          descriptiveName: this.$t("general.phoneNumber"),
          validationRules: "required|numeric|phoneNumberIsrael",
          value: "",
        },
        website: {
          uniqueName: "website",
          descriptiveName: this.$t("general.website"),
          validationRules: "required",
          value: "",
        },
        grades: {
          uniqueName: "grades",
          descriptiveName: this.$t("general.schoolGrades"),
          validationRules: "required",
          value: [],
          inputType: "select",
          selectItems: SCHOOL_GRADES_ITEMS,
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

    submitSchoolDetails() {
      let schoolDataPayload = this.createSchoolSubmitPayload()
      this.postSchoolData(schoolDataPayload)
    },

    createSchoolSubmitPayload() {
      let payload = new FormData()
      payload.append("slug", this.schoolSlug)
      payload.append("name", this.textFields.name.value)
      payload.append("address", this.textFields.street.value)
      payload.append("address_city", this.textFields.city.value)
      payload.append("zip_city", this.textFields.zipCode.value)
      payload.append("school_code", this.textFields.schoolCode.value)
      payload.append("description", this.textFields.description.value)
      payload.append("contact_phone", this.textFields.contactPhone.value)
      payload.append("website", this.textFields.website.value)
      payload.append(
        "grade_levels",
        JSON.stringify(this.textFields.grades.value)
      )
      if (this.profilePicFile) {
        payload.append("profile_picture", this.profilePicFile)
      }
      return payload
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
