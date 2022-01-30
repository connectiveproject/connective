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
        <h3
          class="text-subtitle-2 text-lg-subtitle-1"
          :id="`${uniqueName}-header`"
        >
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
              :autofocus="drawerOpened"
              :value="value"
              :error-messages="errors"
              :id="`${uniqueName}-field`"
              :aria-labelledby="`${uniqueName}-header ${uniqueName}-field`"
              @input="$emit('input', $event)"
            >
            </v-text-field>
            <v-textarea
              v-if="type === 'textarea'"
              v-show="isDrawerOpen()"
              class="mt-5"
              :data-testid="uniqueName"
              :autofocus="drawerOpened"
              :value="value"
              :error-messages="errors"
              :id="`${uniqueName}-field`"
              :aria-labelledby="`${uniqueName}-header ${uniqueName}-field`"
              @input="$emit('input', $event)"
            >
            </v-textarea>
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
              :id="`${uniqueName}-field`"
              :aria-labelledby="`${uniqueName}-header ${uniqueName}-field`"
              @input="$emit('input', $event)"
            />
            <!--
              We are binding 'valueData' with vinitialTags.sync rather than binindg 'value'
              to avoid two-way binding of props. See here:
              https://vuejs.org/v2/guide/components-custom-events.html#sync-Modifier
            -->
            <tags-input
              v-if="type === 'tags'"
              class="mt-5"
              :initialTags.sync="valueData"
              :data-testid="uniqueName"
              @tagsSelected="$emit('update:valueData', $event)"
              :editable="isDrawerOpen()"
            />
            <strong
              v-show="!isDrawerOpen() && type !== 'tags'"
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
import TagsInput from "@/components/TagsInput"
import cloneDeep from "lodash/cloneDeep"

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    TagsInput,
  },
  created() {
    this.valueData = cloneDeep(this.value)
  },
  props: {
    type: {
      type: String,
      required: false,
      default: "text",
      validator: value => {
        return ["text", "textarea", "select", "tags"].includes(value)
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
      valueData: undefined,
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
