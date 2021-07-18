<template>
  <div>
    <h1 v-text="$t('myActivity.myGroups')" class="mb-5" />
    <h2
      v-text="$t('myActivity.hereYouCanSeeTheGroupsYouJoined')"
      class="pb-12"
    />
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
          hide-star
          hide-button
          :title="group.name"
          :subtitle="group.activityName"
          :imgUrl="group.activityLogo"
          :button-text="$t('myActivity.forGroupDetails')"
        >
          <title-to-text
            class="mb-1"
            :title="$t('general.description')"
            :text="trimText(group.description, 21) || $t('errors.empty')"
          />
          <title-to-text
            :title="$t('myActivity.instructorName')"
            :text="group.instructorName || $t('errors.unassigned')"
          />
        </info-card>
      </v-col>
    </v-row>
    <div class="text-center pt-10 overline">
      {{ totalGroups }} {{ $t("myActivity.groupsFound") }}
    </div>
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>
<script>
import store from "../../vuex/store"
import { mapActions, mapState } from "vuex"
import { trimText } from "../../filters"
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
    await store.dispatch("consumerProgramGroup/getGroupList", {
      groupType: SERVER.programGroupTypes.standard,
      override: true,
    })
    next()
  },
  computed: {
    ...mapState("consumerProgramGroup", ["totalGroups", "groupList"]),
    ...mapState("pagination", ["page"]),
  },
  methods: {
    ...mapActions("pagination", ["incrementPage"]),
    ...mapActions("consumerProgramGroup", ["getGroupList"]),
    trimText,
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
