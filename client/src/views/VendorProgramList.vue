<template>
  <div class="">
    <v-row>
      <v-col cols="12" md="8">
        <h1 v-text="$t('myActivity.myPrograms')" class="mb-5" />
        <h2
          v-text="$t('program.hereYouCanSeeAllTheProgramsListedUnderYou')"
          class="pb-12"
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-btn
          data-testid="program-create-btn"
          tile
          large
          class="d-block mx-auto"
          color="success"
          @click="$router.push({ name: 'VendorProgramCreator' })"
        >
          {{ $tc("userActions.add", 1) }}
          <v-icon right> mdi-plus </v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row class="pt-10 ml-0" justify="space-around">
      <v-col
        cols="12"
        sm="6"
        lg="4"
        class="py-10"
        v-for="program in programList"
        :key="program.id"
      >
        <info-card
          :hideStar="true"
          :title="program.name"
          :subtitle="program.domain ? $t(`programFilters.${camelCase(program.domain)}`) : $t('errors.domainUnspecified')"
          :imgUrl="program.logo"
          :buttonText="$t('program.toProgramPage')"
          buttonColor="primary"
          @click="
            $router.push({
              name: 'VendorDetailProgram',
              params: { programSlug: program.slug },
            })
          "
        >
          {{ program.description | trimText(70) }}
        </info-card>
      </v-col>
    </v-row>
    <div class="text-center pt-10 overline">
      {{ programList.length }} {{ $t("program.programsFound") }}
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex"
import camelCase from "lodash/camelCase"
import store from "../vuex/store"
import InfoCard from "../components/InfoCard"

export default {
  components: {
    InfoCard,
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("vendorProgram/getProgramList")
    next()
  },
  computed: {
    ...mapState("vendorProgram", ["programList"]),
  },
  methods: {
    camelCase,
  }
}
</script>
