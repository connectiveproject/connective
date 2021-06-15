<template>
  <div>
    <h1 v-text="$t('myActivity.myGroups')" class="mb-5" />
    <h2
      v-text="
        $t(
          'myActivity.hereYouCanSeeAllTheGroupsOfTheRunningProgramsOfTheSchool'
        )
      "
      class="pb-12"
    />
    <v-row class="pt-10 ml-0" justify="space-around">
      <v-col
        cols="12"
        sm="6"
        lg="4"
        class="py-10"
        v-for="group in groups"
        :key="group.id"
      >
        <info-card
          :starred="false"
          :hideStar="true"
          :title="group.name"
          :subtitle="group.activityName"
          :body="group.description"
          :imgUrl="group.activityLogo"
        >
          <title-to-text
            :title="$t('general.description')"
            :text="group.description || $t('errors.dataUnavailable')"
          />
          <title-to-text
            :title="$t('myActivity.studentsNumberInGroup')"
            :text="group.consumers.length"
          />
          <title-to-text
            :title="$t('myActivity.guideName')"
            :text="group.guide || $t('errors.dataUnavailable')"
          />
        </info-card> </v-col
    ></v-row>
    <!-- TODO: add count of students & guide -->
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>

<script>
import store from "../vuex/store"
import { mapActions, mapState } from "vuex"
import EndOfPageDetector from "../components/EndOfPageDetector"
import InfoCard from "../components/InfoCard"
import TitleToText from "../components/TitleToText.vue"

export default {
  components: {
    EndOfPageDetector,
    InfoCard,
    TitleToText,
  },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("pagination/flushState")
    const groups = await store.dispatch("programsGroups/getGroupList")
    next(vm => {
      vm.groups = groups
    })
  },
  computed: {
    ...mapState("programsGroups", ["totalGroups"]),
    ...mapState("pagination", ["page"]),
  },
  methods: {
    ...mapActions("pagination", ["incrementPage"]),
    ...mapActions("programsGroups", ["getGroupList"]),
    onEndOfPage() {
      this.incrementPage()
    },
    async fetchGroups() {
      if (this.groups.length < this.totalGroups) {
        this.groups = await this.getGroupList(false)
      }
    },
  },
  data() {
    return {
      groups: [],
    }
  },
  watch: {
    page() {
      this.fetchGroups()
    },
  },
}
</script>
