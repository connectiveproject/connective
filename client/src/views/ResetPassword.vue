<template>
  <div>
    <v-card class="absolute-center py-12 px-7" width="320" elevation="16">
      <v-card-title class="text-h5 justify-center mb-6">
        {{
          mode === "init"
          ? $t("general.welcomeToConnective")
          : $t("auth.passwordReset")
        }}
      </v-card-title>
      <v-card-subtitle
        v-if="mode === init"
        class="text-h6 text-center mb-8"
      >
        {{ $t("auth.toStartPleaseChooseNewPassword") }}
      </v-card-subtitle>
      <validation-observer v-slot="{ invalid }">
        <form @submit.prevent="onSubmit">
          <validation-provider
            v-slot="{ errors }"
            name="password"
            rules="required|noHebrew|noArabic|strongPass"
          >
            <v-text-field
              autofocus
              class="mt-5"
              v-model="password"
              :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
              :error-messages="errors"
              :type="showPass ? 'text' : 'password'"
              name="password"
              :label="$t('auth.newPassword')"
              @click:append="showPass = !showPass"
            />
          </validation-provider>

          <validation-provider
            v-slot="{ errors }"
            name="passwordConfirmation"
            rules="required|passConfirm:@password"
          >
            <v-text-field
              class="mt-5"
              v-model="passwordConfirmation"
              :error-messages="errors"
              type="password"
              name="passwordConfirmation"
              :label="$t('auth.reEnterPassword')"
            />
            <div class="overline line-height-1-7 pt-3">
              * {{ $t("auth.chooseAPasswordYouWillRemember") }}.
            </div>
            <div class="overline line-height-1-7 pt-2">
              * {{ $t("errors.strongPassHint") }}.
            </div>
          </validation-provider>
          <validation-provider
            v-if="mode === 'init'"
            v-slot="{ errors }"
            name="tou"
            :rules="{ required: { allowFalse: false } }"
          >
            <v-checkbox
              v-model="isTermsOfUseAgreementAccepted"
              name="tou"
              color="primary"
              :error-messages="errors"
            >
                  <template v-slot:label>
                    <div>
                      {{ $t("general.iAcceptThe") }}
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                          <a
                            target="_blank"
                            @click.stop="isTermsModalOpen = true"
                            v-on="on"
                          >
                            {{ $t("termsOfUse.termsOfUse") }}
                          </a>
                        </template>
                        {{ $t("userActions.clickToRead") }}
                      </v-tooltip>
                    </div>
                  </template>
                </v-checkbox>
          </validation-provider>
          <v-btn
            class="white--text mt-6"
            type="submit"
            color="primary"
            elevation="3"
            v-text="$t('auth.finishRegistration')"
            :disabled="invalid"
            block
          />
          <v-btn
            outlined
            block
            to="/"
            class="mt-4"
            color="primary"
            elevation="3"
            v-text="$t('general.homepage')"
          />
        </form>
      </validation-observer>
    </v-card>
    <modal
      :redirectUrl="modalRedirectUrl"
      v-show="popupMsg !== ''"
      @close="popupMsg = ''"
    >
      {{ popupMsg }}
      <template v-if="modalRedirectUrl" v-slot:btn>
        {{ $t("general.homepage") }}
      </template>
    </modal>
    <detail-modal min-width="300" :title="$t('termsOfUse.termsOfUse')" v-model="isTermsModalOpen">
      <div class="terms-of-use-text mt-8">
        {{ $t('termsOfUse.termsOfUseText') }}
      </div>
      </detail-modal>
  </div>
</template>
<script>
import { mapActions } from "vuex"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import debounce from "lodash/debounce"
import Api from "@/api"
import Modal from "@/components/Modal"
import DetailModal from "@/components/DetailModal"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    Modal,
    DetailModal,
  },
  props: {
    mode: {
      type: String,
      validator(value) {
        return ["init", "recover"].includes(value)
      }
    },
    uid: {
      type: String,
      required: true,
    },
    token: {
      type: String,
      required: true,
    },
  },

  data: () => ({
    isTermsModalOpen: false,
    showPass: false,
    popupMsg: "",
    identityNumber: "",
    password: "",
    passwordConfirmation: "",
    isTermsOfUseAgreementAccepted: false,
    // for redirection to login screen on success
    modalRedirectUrl: "",
  }),

  methods: {
    ...mapActions("auth", ["resetPassword", "login"]),
    ...mapActions("user", ["getUserDetails", "updateUserDetails"]),
    ...mapActions("snackbar", ["showMessage"]),
    onSubmit: debounce(
      function () {
        this.resetPassword({
          uid: this.uid,
          token: this.token,
          pass: this.password,
          passConfirm: this.passwordConfirmation,
        })
          .then(this.handleSubmitSuccess)
          .catch(this.handleSubmitError)
      },
      500,
      { leading: true, trailing: false }
    ),
    async handleSubmitSuccess({ email }) {
      // login after reset pass
      try {
        this.showMessage(this.$t("auth.registrationSucceeded"))
        await this.login({ email, password: this.password, redirect: false })
        if (this.mode === "init") {
          const userDetails = await this.getUserDetails()
          await this.updateUserDetails({ slug: userDetails.slug, userDetails: { isTermsOfUseAgreementAccepted: this.isTermsOfUseAgreementAccepted } })
        }
        this.$router.push({ name: "Dashboard" })
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
    handleSubmitError(msg) {
      try {
        if (msg.response.status === 400) {
          this.handleBadRequestResponse(msg)
        } else {
          this.$router.push({ name: "Error" })
        }
      } catch (err) {
        this.$router.push({ name: "Error" })
      }
    },
    handleBadRequestResponse(msg) {
      // handle status 400 server response
      // redirect on form expiry, display popup msg otherwise
      let errorKeys = Object.keys(msg.response.data)
      if (errorKeys.includes("uid") || errorKeys.includes("token")) {
        this.$router.push({
          name: "Error",
          params: { bodyKey: "auth.registrationFormExpired" },
        })
      } else {
        // display the message received from the server
        this.popupMsg = msg.response.data[errorKeys[0]][0]
      }
    },
  },
}
</script>
<style scoped>
.terms-of-use-text {
    white-space: pre-line;
}
</style>
