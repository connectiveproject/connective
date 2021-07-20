<template>
  <div>
    <v-card class="absolute-center py-12 px-7" width="320" elevation="16">
      <v-card-title class="text-h4 justify-center mb-6">{{
        $t("general.connective")
      }}</v-card-title>
      <v-card-subtitle class="text-h6 text-center mb-8">{{
        $t("auth.chooseNewPassword")
      }}</v-card-subtitle>
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
              :label="$t('auth.newPassword')"
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
              color="primary"
              elevation="3"
              :disabled="invalid"
            >
              {{ $t("auth.finishRegistration") }}
            </v-btn>
          </div>
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
  </div>
</template>
<script>
import { mapActions } from "vuex"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import debounce from "lodash/debounce"
import Modal from "../components/Modal"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    Modal,
  },

  props: {
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
