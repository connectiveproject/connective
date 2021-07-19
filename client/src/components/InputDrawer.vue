<template>
  <div
    data-testid="input-drawer"
    class="drawer white-bg pt-3"
    @click="openDrawer"
    v-click-outside="{
      handler: closeDrawer,
      include: clickOutsideInclude,
    }"
  >
    <v-row dense justify="space-between">
      <v-col cols="2" sm="2">
        <h3 class="text-subtitle-2 text-lg-subtitle-1">
          {{ label }}
        </h3>
      </v-col>
      <v-col cols="7" class="overflow-hidden">
        <validation-observer slim>
          <validation-provider
            immediate
            vid="uniqueName"
            v-slot="{ errors }"
            :name="uniqueName"
            :rules="rules"
          >
            <v-text-field
              v-if="type === 'text'"
              v-show="isDrawerOpen()"
              class="mt-5"
              :data-testid="uniqueName"
              :value="value"
              :error-messages="errors"
              @input="$emit('input', $event)"
            >
            </v-text-field>
            <v-select
              v-if="type === 'select'"
              v-show="isDrawerOpen()"
              chips
              deletable-chips
              class="mt-5"
              :data-testid="uniqueName"
              :value="value"
              :error-messages="errors"
              :items="choices"
              :multiple="multiselect"
              @input="$emit('input', $event)"
            />
            <strong
              v-show="!isDrawerOpen()"
              class="text-subtitle-2 text-lg-subtitle-1"
              :class="{ 'red--text': errors[0] }"
            >
              {{ errors[0] || displayValue | trimText(45) }}
            </strong>
          </validation-provider>
        </validation-observer>
      </v-col>
      <v-col cols="1">
        <v-icon v-show="!isDrawerOpen()">mdi-pencil</v-icon>
      </v-col>
    </v-row>
    <v-divider class="mt-3"></v-divider>
  </div>
</template>
<script>
import { ValidationObserver, ValidationProvider } from "vee-validate"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },

  props: {
    type: {
      type: String,
      required: false,
      default: "text",
      validator: value => {
        return ["text", "select"].includes(value)
      },
    },
    uniqueName: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    rules: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Array, Number],
      required: true,
    },
    choices: {
      // items for input type 'select'. Format: [{ value: 1, text: 'Option 1' }, { ... }]
      type: Array,
      required: false,
    },
    multiselect: {
      type: Boolean,
      default: true,
    },
  },

  data() {
    return {
      drawerOpened: false,
    }
  },

  methods: {
    openDrawer() {
      this.drawerOpened = true
    },
    closeDrawer() {
      this.drawerOpened = false
    },
    isDrawerOpen() {
      return this.drawerOpened
    },
    clickOutsideInclude() {
      // don't collapse input-drawer if click happened inside v-select
      return [...document.getElementsByClassName("menuable__content__active")]
    },
  },

  computed: {
    displayValue() {
      if (this.type === "select") {
        // display textual values of the selected items
        let displayValues = []
        for (let item of this.choices) {
          if (this.value.includes(item.value)) {
            displayValues.push(item.text)
          }
        }
        return displayValues.join(", ")
      }
      return this.value
    },
  },
}
</script>
<style style="scss" scoped>
.drawer:hover {
  background-color: rgb(245, 245, 245);
  cursor: pointer;
  transform: scale(1.05);
}
</style>
