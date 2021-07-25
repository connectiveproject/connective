<template>
  <div class="w-100">
    <v-row class="pt-10 ml-0">
      <v-col cols="3" class="d-none right-pane white-bg">
        <pagination-checkbox-group
          v-for="filter in CONSUMER_LIST_CHECKBOX_FILTERS"
          :key="filter.id"
          :name="filter.name"
          :title="filter.readableName"
          :items="filter.options"
          class="checkbox-group"
        />
      </v-col>
      <v-col cols="12" :class="{ 'px-10': !$vuetify.breakpoint.mobile }">
        <h1 v-text="$t('myActivity.studentsDisplay')" class="pb-6" />
        <pagination-search-bar class="search-bar mx-auto pt-16" />
        <div class="text-center pt-10 overline">
          {{ totalStudents }} {{ $t("myActivity.studentsFound") }}
        </div>
        <v-row
          dense
          justify="space-between"
          class="cards-wrapper mx-auto py-10"
        >
          <v-col
            cols="12"
            sm="6"
            lg="4"
            class="py-10"
            v-for="consumer in studentList"
            :key="consumer.id"
          >
            <info-card
              hide-star
              hide-button
              img-height="0"
              :img-url="null"
              :title="consumer.name"
              :subtitle="$t(`gender.${consumer.profile.gender.toLowerCase()}`)"
              :button-text="$t('myActivity.toThePersonalPage')"
              @click="
                $router.push({
                  name: 'ConsumerDetail',
                  params: { slug: consumer.slug },
                })
              "
            >
              <avatar
                class="mx-auto d-block"
                style="width: 200px"
                :avatar-options="consumer.profile.profilePicture"
              />
            </info-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex"
import store from "../../vuex/store"
import InfoCard from "../../components/InfoCard"
import PaginationCheckboxGroup from "../../components/PaginationCheckboxGroup"
import PaginationSearchBar from "../../components/PaginationSearchBar"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import { CONSUMER_LIST_CHECKBOX_FILTERS } from "./constants"
import Avatar from "../../components/Avatar/Avatar"

export default {
  components: {
    InfoCard,
    PaginationCheckboxGroup,
    PaginationSearchBar,
    EndOfPageDetector,
    Avatar,
  },

  async beforeRouteEnter(to, from, next) {
    await store.dispatch("pagination/updatePagination", { itemsPerPage: 6 })
    await store.dispatch("school/getStudentList", true)
    next()
  },

  computed: {
    ...mapState("school", ["totalStudents", "studentList"]),
  },

  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("pagination", ["incrementPage", "updatePagination"]),
    ...mapActions("school", ["getStudentList"]),

    onEndOfPage() {
      // trigger load on end of page
      this.recentlyScrolled = true
      this.incrementPage()
    },

    async getConsumers() {
      if (this.recentlyScrolled) {
        this.recentlyScrolled = false
        if (this.totalStudents > this.studentList.length) {
          // add new if there are items left to fetch. do not override.
          this.getStudentList(false)
        }
      } else {
        // fetch & ovrride programs list
        this.updatePagination({ page: 1 })
        this.getStudentList(true)
      }
    },
  },

  data() {
    return {
      CONSUMER_LIST_CHECKBOX_FILTERS,
      recentlyScrolled: false,
    }
  },

  watch: {
    "$store.state.pagination": {
      // re-fetch if pagination changed
      deep: true,
      handler() {
        this.getConsumers()
      },
    },
  },
}
</script>

<style lang="scss" scoped>
.cards-wrapper {
  max-width: 1200px;
}
.right-pane {
  border-left: $light-grey 1px solid;
}
.checkbox-group {
  float: right;
  width: 100%;
}
.checkbox-small::v-deep label {
  font-size: 12px;
}
.search-bar {
  max-width: 450px;
}
</style>
