<template>
  <v-dialog v-model="value" persistent max-width="360px">
    <v-card>
      <v-card-title class="headline pt-13 justify-center" v-text="title" />
      <validation-observer v-slot="{ invalid }" ref="observer">
        <form class="form mx-auto" @submit.prevent="save">
          <v-card-text>
            <v-row>
              <v-col class="mt-8" cols="12">
                <validation-provider
                  v-slot="{ errors }"
                  name="name"
                  rules="required"
                >
                  <v-text-field
                    :label="$t('general.name')"
                    v-model="formInput.name"
                    :error-messages="errors"
                  ></v-text-field>
                </validation-provider>
              </v-col>
              <v-col class="mt-8" cols="12">
                <validation-provider
                  v-slot="{ errors }"
                  name="email"
                  rules="required|email"
                >
                  <v-text-field
                    :label="$t('general.email')"
                    v-model="formInput.email"
                    :error-messages="errors"
                  ></v-text-field>
                </validation-provider>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions class="pb-5 mt-12">
            <v-spacer></v-spacer>
            <v-btn color="primary" text @click="close" type="button">
              {{ $t("userActions.cancel") }}
            </v-btn>
            <v-btn color="primary" text type="submit" :disabled="invalid">
              {{ $t("userActions.save") }}
            </v-btn>
          </v-card-actions>
        </form>
      </validation-observer>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "vuex"
import { ValidationObserver, ValidationProvider } from "vee-validate"
import debounce from "lodash/debounce"
import Api from "../../api"

export default {
  components: {
    ValidationObserver,
    ValidationProvider,
  },

  props: {
    value: {
      // is dialog open
      type: Boolean,
      required: true,
    },
    vendor: {
      type: Object,
      required: false,
    },
    title: {
      type: String,
      default: function () {
        return `${this.$tc("invite.invite", 1)} ${this.$t("general.vendor")}`
      },
    },
    slug: {
      type: String,
      required: false,
    },
  },

  mounted() {
    if (!this.formInput) {
      this.initFormInput()
    }
  },

  data() {
    return {
      formInput: this.vendor,
    }
  },

  watch: {
    vendor(obj) {
      // apply vendor prop values to the form, if received
      this.formInput = obj
    },
  },

  methods: {
    ...mapActions("organization", ["addVendor", "editVendor"]),
    ...mapActions("snackbar", ["showMessage"]),
    initFormInput() {
      this.formInput = {
        name: "",
        email: "",
      }
    },
    close() {
      // clear form, close and notify parent
      this.$refs.observer.reset()
      this.$emit("input", false)
      this.initFormInput()
    },
    save: debounce(
      async function () {
        // save to store and notify parent, close dialog
        try {
          if (this.slug) {
            await this.editVendor({
              slug: this.slug,
              vendor: this.formInput,
            })
            this.showMessage(this.$t("success.userDetailsUpdatedSuccessfully"))
          } else {
            await this.addVendor(this.formInput)
            this.showMessage(this.$t("success.anInvitationWasSentToTheSpecifiedEmailAddress"))
          }
          this.$emit("save", this.formInput)
          this.close()
        } catch (err) {
          this.showMessage(Api.utils.parseResponseError(err))
        }
      },
      500,
      { leading: true, trailing: false }
    ),
  },
}
</script>
<style lang="scss" scoped>
.form {
  width: 86%;
}

.v-card__subtitle,
.v-card__text,
.v-card__title {
  padding: 0;
}
</style>
