<template>
  <div>
    <v-row>
      <v-autocomplete
        v-if="editable"
        chips
        deletable-chips
        multiple
        :items="tagOptions"
        v-model="selectedTags"
        @change="onChange()"
        menu-props="closeOnContentClick"
        :label="$t(label)"
        @focus="shortNames = false"
        @blur="shortNames = true"
      ></v-autocomplete>
      <v-chip-group class="chips-group" column v-if="!editable">
        <v-tooltip bottom v-for="chip in selectedTags" :key="chip">
          <template v-slot:activator="{ on, attrs }">
            <v-chip class="filter-chip" v-bind="attrs" v-on="on">
              {{ tagDisplay(chip, true) }}
            </v-chip>
          </template>
          <span>{{ tagDisplay(chip, false) }}</span>
        </v-tooltip>
      </v-chip-group>
    </v-row>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import cloneDeep from "lodash/cloneDeep"
import i18n from "@/plugins/i18n"

export default {
  inheritAttrs: false,
  async created() {
    this.availableTags = await this.loadTags()
    this.selectedTags = cloneDeep(this.initialTags)
  },
  data: () => ({
    selectedTags: [],
    availableTags: [],
    shortNames: true,
  }),
  props: {
    initialTags: {
      type: Array,
      required: false,
    },
    label: {
      type: String,
      default: "",
    },
    editable: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    tagOptions() {
      if (this.shortNames) {
        return this.availableTags.map(tag => {
          return { value: tag.slug, text: this.nameDisplay(tag.name) }
        })
      } else {
        return this.availableTags.map(tag => {
          return {
            value: tag.slug,
            text: `${this.categoryDisplay(tag.category)}:${this.nameDisplay(
              tag.name
            )}`,
          }
        })
      }
    },
  },
  methods: {
    ...mapActions("vxTags", ["loadTags"]),

    nameDisplay(tagName) {
      const key = `tagName.${tagName}`
      return i18n.te(key) ? i18n.t(key) : tagName
    },
    categoryDisplay(tagCategory) {
      const key = `tagCategory.${tagCategory}`
      return i18n.te(key) ? i18n.t(key) : tagCategory
    },
    onChange() {
      this.$emit("tagsSelected", this.selectedTags)
      this.$emit("update:initialTags", this.selectedTags)
    },
    tagDisplay(tagSlug, shortName) {
      const tag = this.availableTags.find(t => t.slug === tagSlug)
      return shortName
        ? this.nameDisplay(tag.name)
        : `${this.categoryDisplay(tag.category)}:${this.nameDisplay(tag.name)}`
    },
  },
}
</script>
