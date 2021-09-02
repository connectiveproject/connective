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
            class="mt-2"
            v-model="email"
            :error-messages="errors"
            :label="$t('general.email')"
          />
        </validation-provider>

        <div class="recaptcha-wrapper">
          <vue-recaptcha
            class="recaptcha"
            ref="recaptcha"
            @verify="onCaptchaVerified"
            @expired="resetCaptcha"
            :loadRecaptchaScript="true"
            sitekey="6LfNaDscAAAAAB6psjQwNmNl_1ZG3OJswmSks0hz"
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
    return { email: "", recaptchaToken: "" }
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
/* .recaptcha {
  transform: scale(0.8);
  transform-origin: 0 0;
} */

/* .recaptcha {
    position: relative;
    width: 100%;
    background: #f9f9f9;
    overflow: hidden;
}

.recaptcha::v-deep * {
    float: right;
    right: 0;
    margin: -2px -2px -10px;
}

.recaptcha::after{
    display: block;
    content: "";
    position: absolute;
    left:0;
    right:150px;
    top: 0;
    bottom:0;
    background-color: #f9f9f9;
    clear: both;
} */
.recaptcha {
  transform: scale(0.9);
  -webkit-transform: scale(0.9);
  transform-origin: center center;
  -webkit-transform-origin: center center;
}
</style>
