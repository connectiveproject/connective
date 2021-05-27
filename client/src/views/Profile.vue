<template>
  <div class="wrapper mt-15 mx-auto px-3">
    <h1 class="mb-5">{{ $t("general.profile") }}</h1>
    <h2 class="pb-12">{{ $t("general.pleaseFillAllDetailsBelow") }}</h2>
    <validation-observer v-slot="{ invalid }">
      <form @submit.prevent="submitProfile">
        <v-row>
          <v-col class="pb-10" cols="12" sm="12" lg="8">
            <input-drawer
              v-for="field in textFields"
              :key="field.id"
              v-model="field.value"
              :uniqueName="field.uniqueName"
              :descriptiveName="field.descriptiveName"
              :validationRules="field.validationRules"
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
import { mapActions } from "vuex"
import store from "../vuex/store"
import { ValidationObserver } from "vee-validate"
import Modal from "../components/Modal"
import InputDrawer from "../components/InputDrawer"
import PictureInput from "../components/PictureInput"
import { personRoundedDrawing } from "../helpers/constants/images"

export default {
  components: {
    ValidationObserver,
    Modal,
    InputDrawer,
    PictureInput,
  },

  async beforeRouteEnter(to, from, next) {
    try {
      // fetch profile data before load
      let profile = await store.dispatch("user/getProfile")
      let userDetails = await store.dispatch("user/getUserDetails")
      let userAttributes = { ...profile, ...userDetails }
      next(vm => vm.setUserAttributes(userAttributes))
    } catch (err) {
      next(vm => (vm.popupMsg = vm.$t("errors.genericError")))
    }
  },

  data() {
    return {
      textFields: {
        firstName: {
          uniqueName: "firstName",
          descriptiveName: this.$t("auth.firstName"),
          validationRules: "required",
          value: "",
        },
        lastName: {
          uniqueName: "lastName",
          descriptiveName: this.$t("auth.lastName"),
          validationRules: "required",
          value: "",
        },
        email: {
          uniqueName: "email",
          descriptiveName: this.$t("general.email"),
          validationRules: "required|email",
          value: "",
        },
        phone: {
          uniqueName: "phone",
          descriptiveName: this.$t("general.phoneNumber"),
          validationRules: "required|numeric|phoneNumberIsrael",
          value: "",
        },
      },
      placeholderPicUrl: personRoundedDrawing,
      profilePicFile: null,
      popupMsg: "",
      id: "",
    }
  },

  methods: {
    ...mapActions("user", ["updateUserDetails"]),
    ...mapActions("coordinator", ["updateProfile"]),
    setUserAttributes(userAttributes) {
      // set user data received from server
      this.id = userAttributes.id
      this.textFields.firstName.value = userAttributes.firstName || ""
      this.textFields.lastName.value = userAttributes.lastName || ""
      this.textFields.email.value = userAttributes.email || ""
      this.textFields.phone.value = userAttributes.phoneNumber || ""
      this.placeholderPicUrl =
        userAttributes.profilePicture || this.placeholderPicUrl
    },

    submitProfile() {
      let userDetailsPayload = this.createUserSubmitPayload()
      let profilePayload = this.createProfileSubmitPayload()
      this.postProfileData(userDetailsPayload, profilePayload)
    },

    createUserSubmitPayload() {
      return {
        id: this.id,
        first_name: this.textFields.firstName.value,
        last_name: this.textFields.lastName.value,
        email: this.textFields.email.value,
      }
    },

    createProfileSubmitPayload() {
      let profilePayload = new FormData()
      profilePayload.append("phone_number", this.textFields.phone.value)
      if (this.profilePicFile) {
        profilePayload.append("profile_picture", this.profilePicFile)
      }
      return profilePayload
    },

    async postProfileData(userDetails, profile) {
      try {
        await this.updateUserDetails({ id: this.id, userDetails })
        await this.updateProfile({ id: this.id, profile })
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
