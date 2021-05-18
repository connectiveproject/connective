<template>
  <div
    class="drawer white-bg pt-3"
    @click="openDrawer"
    v-click-outside="closeDrawer"
  >
    <v-row dense justify="space-between">
      <v-col cols="2" sm="2">
        <h3 class="text-subtitle-2 text-lg-subtitle-1">
          {{ descriptiveName }}
        </h3>
      </v-col>
      <v-col cols="7" lg="4">
        <validation-provider
          vid="uniqueName"
          v-slot="{ errors }"
          :name="uniqueName"
          :rules="validationRules"
          immediate
        >
          <v-text-field
            v-if="inputType === 'text'"
            v-show="isDrawerOpen()"
            class="mt-5"
            :value="value"
            @input="$emit('input', $event)"
            :error-messages="errors"
          >
          </v-text-field>
          <v-select
            v-if="inputType === 'select'"
            v-show="isDrawerOpen()"
            class="mt-5"
            :value="value"
            @input="$emit('input', $event)"
            :error-messages="errors"
            :items="selectItems"
            multiple
            chips
            deletable-chips
          >
          </v-select>
          <strong
            v-show="!isDrawerOpen()"
            class="text-subtitle-2 text-lg-subtitle-1"
            :class="{ 'red--text': errors[0] }"
          >
            {{ errors[0] || displayValue }}
          </strong>
        </validation-provider>
      </v-col>
      <v-col cols="1" sm="1">
        <v-icon v-show="!isDrawerOpen()">mdi-pencil</v-icon>
      </v-col>
    </v-row>
    <v-divider class="mt-3"></v-divider>
  </div>
</template>
<script>
import { ValidationProvider } from "vee-validate"

export default {
  components: {
    ValidationProvider,
  },

  props: {
    inputType: {
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
    descriptiveName: {
      type: String,
      required: true,
    },
    validationRules: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Array],
      required: true,
    },
    selectItems: {
      // items for input type 'select'
      type: Array,
      required: false,
    },
  },

  data: () => ({
    drawerOpened: false,
  }),

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
  },

  computed: {
    displayValue() {
      if (this.inputType === "select") {
        // use the textual values of the items the user selected
        let displayValues = []
        for (let item of this.selectItems) {
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
