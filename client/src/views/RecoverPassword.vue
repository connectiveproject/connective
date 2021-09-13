<template>
  <div>
    <v-card class="absolute-center py-12 px-7" width="350" elevation="16">
      <v-card-title
        class="text-h4 justify-center mb-3 font-weight-bold"
        v-text="$t('auth.passwordReset')"
      />
      <validation-observer
        tag="form"
        ref="observer"
        @submit.prevent="submit"
        v-slot="{ invalid }"
      >
        <validation-provider
          v-slot="{ errors }"
          name="email"
          rules="required|email"
        >
          <v-text-field
            autofocus
            data-testid="email-input"
            class="mt-2"
            v-model="email"
            :error-messages="errors"
            :label="$t('general.email')"
          />
        </validation-provider>

        <div class="pt-3">
          <vue-recaptcha
            class="recaptcha"
            ref="recaptcha"
            loadRecaptchaScript
            @verify="onCaptchaVerified"
            @expired="resetCaptcha"
            :sitekey="RECAPTCHA_SITE_KEY"
          />
        </div>

        <div class="mx-auto d-flex justify-center flex-wrap mt-8 mb-4">
          <v-btn
            class="white--text mb-4"
            type="submit"
            color="primary"
            elevation="3"
            block
            :disabled="invalid || !recaptchaToken"
          >
            {{ $t("auth.reset") }}
          </v-btn>
          <v-btn
            outlined
            type="submit"
            color="primary"
            elevation="3"
            to="/"
            block
          >
            {{ $t("userActions.back") }}
          </v-btn>
        </div>
      </validation-observer>
    </v-card>
  </div>
</template>
<script>
import { mapActions } from "vuex"
import { RECAPTCHA_SITE_KEY } from "@/helpers/constants/constants"
import debounce from "lodash/debounce"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import VueRecaptcha from "vue-recaptcha"
import Api from "@/api"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    VueRecaptcha,
  },

  data() {
    return { email: "", recaptchaToken: "", RECAPTCHA_SITE_KEY }
  },

  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("auth", ["createPasswordRecoveryRequest"]),
    submit: debounce(
      async function () {
        try {
          await this.createPasswordRecoveryRequest({
            email: this.email,
            recaptchaToken: this.recaptchaToken,
          })
          this.showMessage(
            this.$t("success.passwordResetEmailWasSentToYourInbox")
          )
          this.$router.push("/")
        } catch (err) {
          this.resetCaptcha()
          const parsedError = Api.utils.parseResponseError(err)
          if (parsedError.startsWith("email")) {
            return this.showMessage(this.$t("errors.emailAddressNotFound"))
          }
          this.showMessage(parsedError)
        }
      },
      500,
      { leading: true, trailing: false }
    ),
    onCaptchaVerified(recaptchaToken) {
      this.recaptchaToken = recaptchaToken
    },
    resetCaptcha() {
      this.$refs.recaptcha.reset()
      this.recaptchaToken = ""
    },
  },
}
</script>
<style scoped>
.recaptcha {
  transform: scale(0.9);
  -webkit-transform: scale(0.9);
  transform-origin: center center;
  -webkit-transform-origin: center center;
}
</style>
