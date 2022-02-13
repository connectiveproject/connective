<template>
  <div class="ma-3 pa-3 px-lg-16 mx-lg-16 py-lg-6 my-lg-6">
    <v-row>
      <v-col
        cols="12"
        md="8"
        :class="{ 'text-center px-0': $vuetify.breakpoint.xs }"
      >
        <h1 v-text="$t('myActivity.myGroups')" class="px-0 mb-5" />
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
          introjs="add-btn"
          tile
          large
          class="d-block mx-auto"
          color="success"
          data-testid="create-group"
          :block="$vuetify.breakpoint.xs"
          @click="$router.push({ name: 'GroupEditor' })"
        >
          {{ $t("groups.newGroup") }}
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
          :title="group.name"
          :imgUrl="group.activityLogo"
          :buttonText="$t('myActivity.forGroupDetails')"
          buttonColor="primary"
          @click="
            $router.push({
              name: 'GroupDetail',
              params: { groupSlug: group.slug },
            })
          "
        >
          <template v-slot:subtitle>
            {{ group.activityName }}
          </template>
          <title-to-text
            class="mb-1"
            :title="$t('myActivity.groupDescription')"
            :text="trimText(group.description, 21) || $t('errors.empty')"
          />
          <title-to-text
            class="my-0"
            :title="$t('myActivity.studentsNumberInGroup')"
            :text="group.consumers.length"
          />
        </info-card>
      </v-col>
    </v-row>
    <div class="text-center pt-10 overline">
      {{ totalGroups }} {{ $t("myActivity.groupsFound") }}
    </div>
    <end-of-page-detector @end-of-page="onEndOfPage" />
  </div>
</template>
<script>
import store from "@/vuex/store"
import { mapActions, mapState, mapGetters } from "vuex"
import { trimText } from "../../filters"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import InfoCard from "../../components/InfoCard"
import TitleToText from "../../components/TitleToText.vue"
import { SERVER } from "../../helpers/constants/constants"
import introjsSubscribeMixin from "../../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "MyGroups",
  components: {
    EndOfPageDetector,
    InfoCard,
    TitleToText,
  },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("pagination/flushState")
    const schoolSlug = store.getters["school/schoolSlug"]
    await store.dispatch("pagination/addFieldFilter", {
      fieldName: "activity_order__school__slug",
      value: schoolSlug,
    })
    await store.dispatch("programGroup/getGroupList", {
      groupType: [
        SERVER.programGroupTypes.standard,
        SERVER.programGroupTypes.noRegistration,
      ],
      override: true,
      usePagination: true,
    })
    next()
  },
  computed: {
    ...mapState("programGroup", ["totalGroups", "groupList"]),
    ...mapState("pagination", ["page"]),
    ...mapGetters("school", ["schoolSlug"]),
  },
  methods: {
    ...mapActions("pagination", ["incrementPage", "addFieldFilter"]),
    ...mapActions("programGroup", ["getGroupList"]),
    trimText,
    onEndOfPage() {
      this.incrementPage()
    },
    async fetchGroups() {
      this.addFieldFilter({
        fieldName: "activity_order__school__slug",
        value: this.schoolSlug,
      })
      if (this.groupList.length < this.totalGroups) {
        this.getGroupList({
          groupType: [
            SERVER.programGroupTypes.standard,
            SERVER.programGroupTypes.noRegistration,
          ],
          override: false,
          usePagination: true,
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
