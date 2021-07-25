<template>
  <div>
    <v-row class="pt-10 ml-0">
      <v-col
        cols="4"
        md="3"
        class="right-pane white-bg"
        :class="{ 'pr-10': !$vuetify.breakpoint.mobile }"
      >
        <pagination-checkbox-group
          v-for="filter in CONSUMER_PROGRAMS_CHECKBOX_FILTERS"
          :key="filter.id"
          :name="filter.name"
          :title="filter.readableName"
          :items="filter.options"
          class="checkbox-group"
          :class="{ 'checkbox-small': $vuetify.breakpoint.mobile }"
        />
      </v-col>
      <v-col
        cols="8"
        md="9"
        :class="{ 'px-10': !$vuetify.breakpoint.mobile }"
        class="mx-auto"
      >
        <h1 v-text="$t('program.programsExplorer')" class="pb-6" />
        <h3 v-text="$t('program.searchAndFindTheProgramsYouLike!')" />
        <pagination-search-bar class="search-bar mx-auto pt-16" />
        <v-chip-group
          multiple
          color="primary"
          text-color="white"
          v-model="filterTags"
          class="tags-selection mx-auto"
          v-on:change="chipFilterChange"
        >
          <v-chip
            filter
            v-for="tag in CONSUMER_TAGS"
            :key="tag"
            active-class="blue--text"
            :input-value="active"
            @click="toggle"
            class="filter-chip"
          >
            {{ tag }}
          </v-chip>
        </v-chip-group>
        <div class="text-center pt-10 overline">
          {{ totalPrograms }} {{ $t("program.programsFound") }}
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
            v-for="program in programsList"
            :key="program.id"
          >
            <info-card
              :value="program.isConsumerJoined"
              :imgUrl="program.logo"
              :title="program.name"
              :subtitle="getCardSubtitle(program.consumerJoinStatus)"
              :button-text="$t('program.forProgramDetails')"
              @input="e => onStarChange(program, e)"
              @click="openProgram(program.slug)"
            >
              {{ program.description | trimText(70) }}
            </info-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <router-view v-model="isProgramOpen" />
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>

<script>
import Api from "../../api"
import InfoCard from "../../components/InfoCard"
import PaginationSearchBar from "../../components/PaginationSearchBar"
import PaginationCheckboxGroup from "../../components/PaginationCheckboxGroup"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import { mapActions, mapGetters, mapState } from "vuex"
import {
  CONSUMER_PROGRAMS_CHECKBOX_FILTERS,
  CONSUMER_TAGS,
} from "../../helpers/constants/constants"

export default {
  components: {
    PaginationCheckboxGroup,
    InfoCard,
    PaginationSearchBar,
    EndOfPageDetector,
  },

  computed: {
    ...mapState("consumerProgram", ["programsList", "totalPrograms"]),
    ...mapGetters("school", ["schoolSlug"]),
  },

  methods: {
    ...mapActions("pagination", ["incrementPage", "updatePagination", "addFieldFilter", "removeFieldFilter"]),
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("consumerProgram", [
      "getProgramsList",
      "joinProgram",
      "leaveProgram",
    ]),

    onEndOfPage() {
      // trigger programs load on end of page
      this.recentlyScrolled = true
      this.incrementPage()
    },

    openProgram(slug) {
      this.isProgramOpen = true
      this.$router.push({ name: "ConsumerProgramModal", params: { slug } })
    },

    async chipFilterChange() {
      let tagsSelected = []
      if (this.filterTags.length) {
        for (let i = 0; i < this.filterTags.length; i++) {
          tagsSelected.push(CONSUMER_TAGS[this.filterTags[i]])
        }

        await this.addFieldFilter({ fieldName: "tags", value: tagsSelected })
      } else {
        await this.removeFieldFilter("tags")
      }
    },

    async getPrograms() {
      if (this.recentlyScrolled) {
        this.recentlyScrolled = false
        if (this.totalPrograms > this.programsList.length) {
          // add new programs if there are items left to fetch. do not override.
          this.getProgramsList(false)
        }
      } else {
        // fetch & ovrride programs list
        this.updatePagination({ page: 1 })
        this.getProgramsList(true)
      }
    },

    getCardSubtitle(consumerJoinStatus) {
      return `${this.$t("general.status")}: ${
        this.statusToText[consumerJoinStatus]
      }`
    },

    async onStarChange(program, isStarred) {
      // (dis)request a program and change order status accordingly
      try {
        if (isStarred) {
          await this.joinProgram(program.slug)
          return this.showMessage(this.$t("success.joinedProgramSuccessfully"))
        }
        if (program.consumerJoinStatus === "JOINED") {
          return this.showMessage(
            this.$t("errors.cantLeaveProgramAfterGroupAssigned")
          )
        } else {
          await this.leaveProgram(program.slug)
          return this.showMessage(this.$t("success.leftProgramSuccessfully"))
        }
      } catch (err) {
        this.showMessage(Api.utils.parseResponseError(err))
      }
    },
  },

  data() {
    return {
      CONSUMER_PROGRAMS_CHECKBOX_FILTERS,
      CONSUMER_TAGS,
      recentlyScrolled: false,
      filterTags: [],
      isProgramOpen: true,
      statusToText: {
        PENDING_GROUP_ASSIGNMENT: this.$t("program.pendingGroupAssignment"),
        JOINED: this.$t("auth.registered"),
        NOT_JOINED: this.$t("auth.notRegistered"),
      },
    }
  },

  watch: {
    "$store.state.pagination": {
      // re-fetch if pagination changed
      deep: true,
      handler() {
        this.getPrograms()
      },
    },
    isProgramOpen(value) {
      // route back on close
      if (!value) {
        this.$router.push({ name: "ConsumerProgramsExplorer" })
      }
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
.search-bar {
  max-width: 50%;
}

.tags-selection {
  max-width: 50%;
}
.filter-chip {
  margin: 5px;
}
.checkbox-group {
  float: right;
  width: 100%;
}
</style>
