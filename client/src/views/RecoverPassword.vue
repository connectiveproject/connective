<template>
  <div>
    <v-card class="absolute-center py-12 px-7" width="320" elevation="16">
      <v-card-title
        class="text-h4 justify-center mb-3 font-weight-bold"
        v-text="$t('auth.passwordReset')"
      />
      <validation-observer tag="form" ref="observer" @submit.prevent="submit" v-slot="{ invalid }">
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

          <div class="mx-auto d-flex justify-center mt-8 mb-4">
            <v-btn
              class="white--text"
              type="submit"
              color="primary"
              elevation="3"
              :disabled="invalid"
              block
            >
              {{ $t("auth.reset") }}
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
import Api from "@/api"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },

  data() {
    return { email: "" }
  },

  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("auth", ["createPasswordRecoveryRequest"]),
    submit: debounce(
      async function () {
        try {
          await this.createPasswordRecoveryRequest(this.email)
          this.showMessage(this.$t("success.passwordResetEmailWasSentToYourInbox"))
          this.$router.push("/")
        } catch (err) {
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
  },
}
</script>
