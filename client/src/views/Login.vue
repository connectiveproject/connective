<template>
  <div>
    <v-card class="absolute-center py-12 px-7" width="320" elevation="16">
      <v-card-title
        id="letter-spacing-2"
        class="text-h4 justify-center mb-3 font-weight-bold"
        >{{ $t("general.connective") }}</v-card-title
      >
      <validation-observer ref="observer">
        <form @submit.prevent="submit">
          <validation-provider
            v-slot="{ errors }"
            name="email"
            rules="required|email"
          >
            <v-text-field
              data-testid="email-input"
              class="mt-2"
              v-model="email"
              :error-messages="errors"
              :label="$t('general.email')"
              required
            ></v-text-field>
          </validation-provider>
          <validation-provider
            v-slot="{ errors }"
            name="password"
            rules="required"
          >
            <v-text-field
              data-testid="password-input"
              class="mt-2"
              v-model="password"
              :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
              :error-messages="errors"
              :type="showPass ? 'text' : 'password'"
              name="password"
              :label="$t('auth.password')"
              @click:append="showPass = !showPass"
            ></v-text-field>
          </validation-provider>

          <div class="mx-auto d-flex justify-center mt-8 mb-4">
            <v-btn
              data-testid="login-btn"
              class="white--text"
              type="submit"
              color="primary"
              elevation="3"
              block
            >
              {{ $t("auth.login") }}
            </v-btn>
          </div>
        </form>
      </validation-observer>
    </v-card>
    <modal v-show="popupMsg !== ''" @close="popupMsg = ''">
      {{ popupMsg }}
    </modal>
  </div>
</template>
<script>
import { mapActions } from "vuex"
import debounce from "lodash/debounce"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import Modal from "../components/Modal"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    Modal,
  },

  data: () => ({
    showPass: false,
    popupMsg: "",
    email: "",
    password: "",
  }),

  methods: {
    ...mapActions("auth", ["login"]),
    submit: debounce(
      async function () {
        if (!(await this.$refs.observer.validate())) return
        this.login({ email: this.email, password: this.password }).catch(
          this.displayLoginError
        )
      },
      500,
      { leading: true, trailing: false }
    ),
    displayLoginError(msg) {
      try {
        if (
          Object.prototype.hasOwnProperty.call(msg, "response") &&
          Object.prototype.hasOwnProperty.call(msg.response, "data")
        ) {
          let error_msg = msg.response.data.nonFieldErrors[0]
          if (error_msg === "Unable to log in with provided credentials.") {
            this.popupMsg = this.$t("errors.invalidCreds")
            return
          }
        }
        this.popupMsg = this.$t("errors.genericError")
      } catch (err) {
        this.popupMsg = this.$t("errors.genericError")
      }
    },
  },
}
</script>
<style lang="scss" scoped>
#letter-spacing-2 {
  letter-spacing: 2px !important;
}
</style>
