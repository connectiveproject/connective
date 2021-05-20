<template>
  <v-container fill-height>
    <v-row dense justify="center" align="center">
      <v-col cols="11" sm="6" md="6" lg="4" xl="3">
        <v-card class="py-12 px-5 mb-16" elevation="20" outlined>
          <v-card-title
            class="purple--text text--darken-4 text-h4 justify-center mb-6"
            >{{ $t("general.connective") }}</v-card-title
          >
          <v-card-subtitle
            class="purple--text text--darken-4 text-h6 text-center mb-8"
            >{{ $t("auth.registration") }}</v-card-subtitle
          >
          <validation-observer v-slot="{ invalid }">
            <form @submit.prevent="onSubmit">
              <validation-provider
                v-slot="{ errors }"
                name="password"
                rules="required|strongPass"
              >
                <v-text-field
                  class="mt-5"
                  v-model="password"
                  :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
                  :error-messages="errors"
                  :type="showPass ? 'text' : 'password'"
                  name="password"
                  :label="$t('auth.password')"
                  @click:append="showPass = !showPass"
                ></v-text-field>
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
                ></v-text-field>
              </validation-provider>

              <div class="mx-auto d-flex justify-center mt-12">
                <v-btn
                  class="ml-3 white--text"
                  type="submit"
                  color="purple darken-3"
                  elevation="3"
                  :disabled="invalid"
                >
                  {{ $t("auth.finishRegistration") }}
                </v-btn>
              </div>
            </form>
          </validation-observer>
        </v-card>
      </v-col>
    </v-row>
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
  </v-container>
</template>
<script>
import { ValidationObserver, ValidationProvider } from "vee-validate"
import Modal from "../components/Modal"
import { mapActions } from "vuex"
import { server } from "../helpers/constants/constants"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    Modal,
  },

  props: {
    userType: {
      type: String,
      required: true,
      validator: userType => {
        return Object.values(server.userTypes).indexOf(userType) !== -1
      },
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
    userTypesList: server.userTypes,
    showPass: false,
    popupMsg: "",
    identityNumber: "",
    password: "",
    passwordConfirmation: "",
    // for redirection to login screen on success
    modalRedirectUrl: "",
  }),

  methods: {
    ...mapActions("auth", ["resetPassword"]),
    onSubmit() {
      this.resetPassword({
        uid: this.uid,
        token: this.token,
        pass: this.password,
        passConfirm: this.passwordConfirmation,
      })
        .then(this.handleSubmitSuccess)
        .catch(this.handleSubmitError)
    },
    handleSubmitSuccess() {
      this.modalRedirectUrl = "/"
      this.popupMsg = this.$t("auth.registrationSucceeded") + "!"
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
