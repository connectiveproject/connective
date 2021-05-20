<template>
  <v-text-field
    v-model="textInput"
    class="input"
    :label="$t('userActions.search')"
    append-icon="mdi-magnify "
    @click:append="updatePagination({ searchFilter: textInput })"
    @keyup.enter="updatePagination({ searchFilter: textInput })"
  ></v-text-field>
</template>

<script>
import { mapActions } from "vuex"

export default {
  data() {
    return { textInput: "" }
  },
  methods: mapActions("pagination", ["updatePagination"]),
}
</script>
