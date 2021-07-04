<template>
  <div>
    <v-row>
      <v-col cols="12" md="8">
        <h1 v-text="$t('myActivity.myGroups')" class="mb-5" />
        <h2
          v-text="
            $t(
              'myActivity.hereYouCanSeeAllTheGroupsOfTheRunningProgramsOfTheSchool'
            )
          "
          class="pb-12"
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-btn
          tile
          large
          class="d-block mx-auto"
          color="success"
          @click="$router.push({ name: 'GroupEditor' })"
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
        v-for="group in groupList"
        :key="group.id"
      >
        <info-card
          :hideStar="true"
          :title="group.name"
          :subtitle="group.activityName"
          :body="group.description"
          :imgUrl="group.activityLogo"
          :buttonText="$t('myActivity.forGroupDetails')"
          buttonColor="teal"
          @click="
            $router.push({
              name: 'DetailGroup',
              params: { groupSlug: group.slug },
            })
          "
        >
          <title-to-text
            :title="$t('myActivity.groupDescription')"
            :text="group.description || $t('errors.empty')"
          />
          <title-to-text
            :title="$t('myActivity.studentsNumberInGroup')"
            :text="group.consumers.length"
          />
          <title-to-text
            :title="$t('myActivity.instructorName')"
            :text="group.instructorName || $t('errors.unassigned')"
          />
        </info-card>
      </v-col>
    </v-row>
    <div class="text-center pt-10 overline">
      {{ totalGroups }} {{ $t("program.programsFound") }}
    </div>
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>
<script>
import store from "../../vuex/store"
import { mapActions, mapState } from "vuex"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import InfoCard from "../../components/InfoCard"
import TitleToText from "../../components/TitleToText.vue"
import { SERVER } from "../../helpers/constants/constants"

export default {
  components: {
    EndOfPageDetector,
    InfoCard,
    TitleToText,
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("pagination/flushState")
    await store.dispatch("programGroup/getGroupList", {
      groupType: SERVER.programGroupTypes.standard,
      override: true,
    })
    next()
  },
  computed: {
    ...mapState("programGroup", ["totalGroups", "groupList"]),
    ...mapState("pagination", ["page"]),
  },
  methods: {
    ...mapActions("pagination", ["incrementPage"]),
    ...mapActions("programGroup", ["getGroupList"]),
    onEndOfPage() {
      this.incrementPage()
    },
    fetchGroups() {
      if (this.groupList.length < this.totalGroups) {
        this.getGroupList({
          groupType: SERVER.programGroupTypes.standard,
          override: false,
        })
      }
    },
  },
  watch: {
    page() {
      this.fetchGroups()
    },
  },
}
</script>