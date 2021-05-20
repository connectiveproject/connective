<template>
  <v-dialog v-model="value" persistent max-width="360px">
    <v-card>
      <v-card-title class="headline pt-13 justify-center" v-text="title" />
      <validation-observer v-slot="{ invalid }" ref="observer">
        <form class="form mx-auto" @submit.prevent="save">
          <v-card-text>
            <v-row>
              <v-col class="mt-8" cols="12" sm="5">
                <validation-provider
                  v-slot="{ errors }"
                  name="firstName"
                  rules="required"
                >
                  <v-text-field
                    :label="$t('auth.firstName')"
                    v-model="formInput.firstName"
                    :error-messages="errors"
                  ></v-text-field>
                </validation-provider>
              </v-col>
              <v-spacer></v-spacer>
              <v-col class="mt-8" cols="12" sm="7">
                <validation-provider
                  v-slot="{ errors }"
                  name="lastName"
                  rules="required"
                >
                  <v-text-field
                    :label="$t('auth.lastName')"
                    v-model="formInput.lastName"
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
              <v-col class="mt-8" cols="12">
                <validation-provider
                  v-slot="{ errors }"
                  name="phoneNumber"
                  rules="required|phoneNumberIsrael"
                >
                  <v-text-field
                    :label="$t('general.phoneNumber')"
                    v-model="formInput.profile.phoneNumber"
                    :error-messages="errors"
                  ></v-text-field>
                </validation-provider>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions class="pb-5 mt-12">
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="close" type="button">
              {{ $t("userActions.close") }}
            </v-btn>
            <v-btn color="blue darken-1" text type="submit" :disabled="invalid">
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
    student: {
      type: Object,
      required: false,
    },
    title: {
      type: String,
      default: function () {
        return `${this.$tc("invite.invite", 1)} ${this.$t("general.student")}`
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
      formInput: this.student,
    }
  },

  watch: {
    student(obj) {
      // apply student prop values to the form, if received
      this.formInput = obj
    },
  },

  methods: {
    ...mapActions("school", ["addStudent", "editStudent"]),
    initFormInput() {
      this.formInput = {
        idNumber: "",
        firstName: "",
        lastName: "",
        city: "",
        email: "",
        profile: {
          phoneNumber: "",
        },
      }
    },
    close() {
      // clear form, close and notify parent
      this.$refs.observer.reset()
      this.$emit("input", false)
      this.initFormInput()
    },
    async save() {
      // save to store and notify parent, close dialog
      if (this.slug) {
        await this.editStudent({ slug: this.slug, student: this.formInput })
      } else {
        await this.addStudent(this.formInput)
      }
      this.$emit("save", this.formInput)
      this.close()
    },
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
