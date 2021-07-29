<template>
  <v-dialog max-width="600px" v-model="value" persistent>
    <v-card>
      <v-card-title class="headline pt-13 justify-center" v-text="title" />
      <v-card-subtitle
        class="text-subtitle-1 pt-5 text-center"
        v-text="subtitle"
        v-if="subtitle"
      />
      <validation-observer v-slot="{ invalid }" ref="observer">
        <form class="w-75 mx-auto" @submit.prevent="save">
          <v-card-text>
            <v-row>
              <v-col
                v-for="field in formInput"
                :key="field.id"
                class="mt-8"
                cols="12"
                :md="formInput.length > 1 ? 6 : 12"
              >
                <validation-provider
                  v-slot="{ errors }"
                  :name="field.name"
                  :rules="field.rule"
                >
                  <v-select
                    v-if="field.type && field.type === 'select'"
                    class="mx-2"
                    v-model="field.value"
                    :label="field.label"
                    :items="field.choices"
                    :error-messages="errors"
                  />
                  <v-text-field
                    v-else
                    class="mx-2"
                    :label="field.label"
                    v-model="field.value"
                    :error-messages="errors"
                  />
                </validation-provider>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions class="pb-5 mt-12">
            <v-spacer />
            <v-btn color="primary" text @click="close" type="button">
              {{ $t("userActions.close") }}
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
import { ValidationObserver, ValidationProvider } from "vee-validate"
import cloneDeep from "lodash/cloneDeep"

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
    inputFields: {
      // the form's prototype
      // e.g.,  [ { name: 'field1', rule: 'required|size:5000', label: $t('translation'), value: 'placeholderValue' }, { ... }, ... ]
      type: Array,
      required: true,
    },
    title: {
      type: String,
      default: function () {
        return this.$tc("userActions.add", 1)
      },
    },
    subtitle: {
      type: String,
      default: "",
    },
  },

  data() {
    return {
      formInput: this.getInputFields(),
    }
  },

  watch: {
    inputFields: {
      // change local input object according to prop changes
      deep: true,
      handler() {
        this.formInput = this.getInputFields()
      },
    },
  },

  methods: {
    close() {
      // clear errors & close form
      this.$refs.observer.reset()
      this.$emit("input", false)
    },

    save() {
      // notify parent on save & init
      this.$emit("save", this.createFormResult(this.formInput))
      this.formInput = this.getInputFields()
      this.close()
    },

    createFormResult(formInput) {
      // return the user input as { fieldName: userInputValue, ... }
      const formResult = {}
      for (const field of formInput) {
        formResult[field.name] = field.value
      }
      return formResult
    },

    getInputFields() {
      // init based on prop
      return cloneDeep(this.inputFields)
    },
  },
}
</script>

<style lang="scss" scoped>
.v-card__subtitle,
.v-card__text,
.v-card__title {
  padding: 0;
}
</style>
