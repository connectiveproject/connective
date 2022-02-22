<template>
  <v-text-field
    v-model="textInput"
    class="input"
    :label="$t('userActions.search')"
    append-icon="mdi-magnify "
    @click:append="search()"
    @keyup.enter="search()"
  ></v-text-field>
</template>

<script>
import { mapActions } from "vuex"

export default {
  data() {
    return { textInput: "" }
  },
  methods: {
    ...mapActions("pagination", ["updatePagination"]),
    search() {
      this.updatePagination({ searchFilter: this.textInput })
      this.$emit("search", this.textInput)
    },
  },
}
</script>
