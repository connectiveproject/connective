<template>
  <div class="pa-10">
    <v-tabs color="grey darken-4" class="pb-10">
      <v-tab
        :to="{ name: 'ConsumerMyGroups' }"
        v-text="$t('myActivity.activeGroups')"
      />
      <v-tab
        :to="{ name: 'ConsumerMyEvents' }"
        v-text="$t('myActivity.myEvents')"
      />
    </v-tabs>
    <v-row>
      <v-col class="mx-auto" sm="11" lg="9">
        <router-view />
      </v-col>
    </v-row>
  </div>
</template>
