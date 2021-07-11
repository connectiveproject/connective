<template>
  <v-container>
    <v-row dense justify="center">
      <v-col cols="11" sm="6" md="6" lg="4" xl="3">
        <v-card class="mx-auto py-12 px-5 login-card" elevation="20" outlined>
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

              <div class="mx-auto d-flex justify-center mt-16 mb-4">
                <v-btn
                  data-testid="login-btn"
                  class="white--text"
                  type="submit"
                  color="primary"
                  elevation="3"
                >
                  {{ $t("auth.login") }}
                </v-btn>
              </div>
            </form>
          </validation-observer>
        </v-card>
      </v-col>
    </v-row>
    <modal v-show="popupMsg !== ''" @close="popupMsg = ''">
      {{ popupMsg }}
    </modal>
  </v-container>
</template>
<script>
import { mapActions } from "vuex"
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

    submit() {
      this.$refs.observer.validate().then(() => {
        this.login({ email: this.email, password: this.password }).catch(
          this.displayLoginError
        )
      })
    },

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
.login-card {
  margin-top: 120px;
}
#letter-spacing-2 {
  letter-spacing: 2px !important;
}
</style>
