<template>
  <div>
    <v-card class="absolute-center py-12 px-7" width="320" elevation="16">
      <v-card-title
        class="text-h4 justify-center mb-6"
        v-text="$t('auth.detailsCompletion')"
      />
      <v-card-subtitle
        class="text-h6 text-center mb-8"
        v-text="$t('general.personalInfo')"
      />
      <validation-observer
        ref="observer"
        tag="form"
        v-slot="{ invalid }"
        @submit.prevent="submit"
      >
        <validation-provider v-slot="{ errors }" name="name" rules="required">
          <v-text-field
            class="mt-5"
            v-model="registrationInfo.name"
            :error-messages="errors"
            :label="$t('general.name')"
            required
          />
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          name="phone"
          rules="required|numeric|phoneNumberIsrael"
        >
          <v-text-field
            class="mt-5"
            v-model="registrationInfo.phone"
            :error-messages="errors"
            :label="$t('general.phoneNumber')"
            required
          />
        </validation-provider>
        <div class="mx-auto d-flex justify-center mt-12">
          <v-btn
            class="ml-3 white--text"
            type="submit"
            color="primary"
            elevation="3"
            v-text="$t('auth.detailsConfirmation')"
            :disabled="invalid"
          />
          <v-btn
            class="mr-3"
            type="button"
            color="primary"
            elevation="3"
            outlined
            v-text="$t('userActions.toHomepage')"
            @click="logout"
          />
        </div>
      </validation-observer>
    </v-card>
    <modal
      :redirectComponentName="modalRedirectComponentName"
      v-show="popupMsg !== ''"
      @close="popupMsg = ''"
    >
      {{ popupMsg }}
    </modal>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import store from "../../vuex/store"
import Modal from "../../components/Modal"
import Api from "../../api"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    Modal,
  },
  data() {
    return {
      modalRedirectComponentName: "",
      slug: null,
      popupMsg: "",
      registrationInfo: {
        name: "",
        phone: "",
      },
    }
  },

  async mounted() {
    let userDetails = await store.dispatch("user/getUserDetails")
    this.slug = userDetails.slug
  },

  methods: {
    ...mapActions("user", ["updateUserDetails"]),
    ...mapActions("vendor", ["updateProfile"]),
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("auth", ["logout"]),
    submit: debounce(
      async function () {
        try {
          await Promise.all[
            (this.updateProfile({
              slug: this.slug,
              profile: { phoneNumber: this.registrationInfo.phone },
            }),
            this.updateUserDetails({
              slug: this.slug,
              userDetails: { name: this.registrationInfo.name },
            }))
          ]
          this.modalRedirectComponentName = "VendorProfile"
          this.popupMsg = this.$t("general.detailsSuccessfullyUpdated")
        } catch (err) {
          const message = Api.utils.parseResponseError(err)
          this.showMessage(message)
        }
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>

<style lang="scss" scoped>
.v-card__subtitle,
.v-card__text,
.v-card__title {
  padding: 0;
}
</style>
