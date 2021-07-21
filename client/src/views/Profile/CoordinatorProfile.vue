<template>
  <div class="wrapper mt-15 mx-auto px-3">
    <h1 class="mb-5">{{ $t("general.myProfile") }}</h1>
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
              :label="field.label"
              :rules="field.rules"
            />
          </v-col>
          <v-col cols="12" sm="12" lg="3">
            <editable-avatar class="mx-auto avatar" v-model="profilePicture" />
          </v-col>
        </v-row>
        <v-btn
          class="my-16 py-5 white--text"
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
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import store from "../../vuex/store"
import { ValidationObserver } from "vee-validate"
import Modal from "../../components/Modal"
import InputDrawer from "../../components/InputDrawer"
import EditableAvatar from "../../components/Avatar/EditableAvatar"

export default {
  components: {
    ValidationObserver,
    Modal,
    InputDrawer,
    EditableAvatar,
  },

  async beforeRouteEnter(to, from, next) {
    try {
      // fetch profile data before load
      let profile = await store.dispatch("coordinator/getProfile")
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
        name: {
          uniqueName: "name",
          label: this.$t("general.name"),
          rules: "required",
          value: "",
        },
        email: {
          uniqueName: "email",
          label: this.$t("general.email"),
          rules: "required|email",
          value: "",
        },
        phone: {
          uniqueName: "phone",
          label: this.$t("general.phoneNumber"),
          rules: "required|numeric|phoneNumberIsrael",
          value: "",
        },
      },
      profilePicture: {},
      popupMsg: "",
      slug: "",
    }
  },

  methods: {
    ...mapActions("user", ["updateUserDetails"]),
    ...mapActions("coordinator", ["updateProfile"]),
    setUserAttributes(userAttributes) {
      // set user data received from server
      this.slug = userAttributes.slug
      this.textFields.name.value = userAttributes.name || ""
      this.textFields.email.value = userAttributes.email || ""
      this.textFields.phone.value = userAttributes.phoneNumber || ""
      this.profilePicture = userAttributes.profilePicture || {}
    },

    submitProfile: debounce(
      function () {
        let userDetailsPayload = this.createUserSubmitPayload()
        let profilePayload = this.createProfileSubmitPayload()
        this.postProfileData(userDetailsPayload, profilePayload)
      },
      500,
      { leading: true, trailing: false }
    ),

    createUserSubmitPayload() {
      return {
        name: this.textFields.name.value,
        email: this.textFields.email.value,
      }
    },

    createProfileSubmitPayload() {
      return {
        phoneNumber: this.textFields.phone.value,
        profilePicture: this.profilePicture,
      }
    },

    async postProfileData(userDetails, profile) {
      try {
        await this.updateUserDetails({ slug: this.slug, userDetails })
        await this.updateProfile({ slug: this.slug, profile })
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
  },
}
</script>
<style lang="scss" scoped>
.wrapper {
  width: 90%;
}
.avatar {
  max-width: 350px;
}
</style>
