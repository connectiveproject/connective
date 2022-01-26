<template>
  <div>
    <v-autocomplete
      v-if="editable"
      chips
      deletable-chips
      multiple
      :items="tagOptions"
      v-model="selectedTags"
      @change="onChange()"
    ></v-autocomplete>
    <v-chip-group class="chips-group" v-if="!editable">
      <v-tooltip bottom v-for="chip in selectedTags" :key="chip">
        <template v-slot:activator="{ on, attrs }">
          <v-chip class="filter-chip" v-bind="attrs" v-on="on">
            {{ tagDisplay(chip, true) }}
          </v-chip>
        </template>
        <span>{{ tagDisplay(chip, false) }}</span>
      </v-tooltip>
    </v-chip-group>
  </div>
</template>

<script>
import i18n from "@/plugins/i18n"
import { mapActions } from "vuex"
import cloneDeep from "lodash/cloneDeep"

export default {
  inheritAttrs: false,
  async created() {
    this.availableTags = await this.loadTags()
    this.selectedTags = cloneDeep(this.initialTags)
  },
  data: () => ({
    selectedTags: [],
    availableTags: [],
    shortNames: false,
  }),
  props: {
    initialTags: {
      type: Array,
      required: false,
    },
    label: {
      type: String,
      default: i18n.t("tags.tag"),
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
          return { value: tag.slug, text: tag.name }
        })
      } else {
        return this.availableTags.map(tag => {
          return { value: tag.slug, text: `${tag.category}:${tag.name}` }
        })
      }
    },
  },
  methods: {
    ...mapActions("vxTags", ["loadTags"]),

    onChange() {
      this.$emit("tagsSelected", this.selectedTags)
      this.$emit("update:initialTags", this.selectedTags)
    },
    tagDisplay(tagSlug, shortName) {
      const tag = this.availableTags.find(t => t.slug === tagSlug)
      return shortName ? tag.name : `${tag.category}:${tag.name}`
    },
  },
}
</script>
