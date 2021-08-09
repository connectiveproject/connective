<template>
  <v-card :elevation="elevation">
    <v-card-text>
      <validation-observer ref="observer">
        <v-row>
          <v-col
            v-for="(field, i) in value"
            :key="i"
            class="mt-8"
            cols="12"
            md="6"
          >
            <validation-provider
              v-slot="{ errors }"
              :name="field.name"
              :rules="field.rules"
            >
              <v-select
                v-if="field.type && field.type === 'select'"
                class="mx-2"
                :data-testid="field.name"
                :label="field.label"
                :error-messages="errors"
                :value="field.value"
                :items="field.choices"
                @input="input => updateField(i, input)"
                :multiple="field.multiselect"
              />
              <v-textarea
                v-else-if="field.type && field.type === 'textarea'"
                class="mx-2"
                auto-grow
                rows="1"
                :data-testid="field.name"
                :label="field.label"
                :error-messages="errors"
                :value="field.value"
                @input="input => updateField(i, input)"
              />
              <v-text-field
                v-else
                class="mx-2"
                :data-testid="field.name"
                :label="field.label"
                :error-messages="errors"
                :value="field.value"
                @input="input => updateField(i, input)"
              />
            </validation-provider>
          </v-col>
        </v-row>
      </validation-observer>
    </v-card-text>
  </v-card>
</template>

<script>
import Vue from "vue"
import { ValidationObserver, ValidationProvider } from "vee-validate"

export default {
  components: {
    ValidationObserver,
    ValidationProvider,
  },

  props: {
    value: {
      // the form's prototype
      // e.g.,  [ { name: 'field1', rules: 'required|size:5000', label: $t('translation'), value: 'placeholderValue' }, { ... }, ... ]
      type: Array,
      required: true,
    },
    elevation: {
      type: [Number, String],
      default: 2,
    },
  },

  watch: {
    value: {
      // emit validation events
      deep: true,
      async handler() {
        await Vue.nextTick()
        const isValid = await this.$refs.observer.validate({ silent: true })
        if (isValid) {
          this.$emit("valid")
        } else {
          this.$emit("invalid")
        }
      },
    },
  },

  methods: {
    updateField(fieldIndex, input) {
      // v-model implementation
      const fields = [...this.value]
      fields[fieldIndex].value = input
      this.$emit("input", fields)
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
