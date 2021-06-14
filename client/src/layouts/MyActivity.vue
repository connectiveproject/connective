<template>
  <v-tabs color="accent-4" class="pa-10">
    <v-tab v-text="$t('myActivity.activeGroups')" />
    <v-tab v-text="$t('myActivity.myEvents')" />
    <v-tab v-text="$t('myActivity.myPrograms')" />

    <v-tab-item>
      <my-groups />
    </v-tab-item>
    <v-tab-item> האירועים שלי </v-tab-item>
    <v-tab-item> התוכניות שלי </v-tab-item>
  </v-tabs>
</template>

<script>
import MyGroups from "../views/MyGroups"
export default {
  components: { MyGroups },
}
</script>

<style></style>
