<template>
  <div>
    <side-drawer
      v-model="filterDrawer"
      :title="$t('filter.programsFiltering')"
      :subtitle="$t('filter.clickToFilter')"
    >
      <pagination-checkbox-group
        v-for="filter in PROGRAMS_CHECKBOX_FILTERS"
        :key="filter.id"
        :name="filter.name"
        :title="filter.readableName"
        :items="filter.options"
        class="checkbox-group"
        :class="{ 'checkbox-small': $vuetify.breakpoint.xs }"
      />
    </side-drawer>
    <div class="ma-3 pa-3 px-lg-16 mx-lg-16 py-lg-6 my-lg-6">
      <div class="mx-auto mx-sm-16 d-flex justify-space-between flex-wrap">
        <div class="pb-7">
          <h1 v-text="$t('program.programCatalog')" class="pb-6" />
          <h3 v-text="$t('program.searchAndFindTheProgramsYouLike!')" />
        </div>
        <v-btn
          introjs="advanced-search"
          class="mx-auto mx-md-0 primary mt-10 mt-md-0"
          :block="$vuetify.breakpoint.xs"
          v-text="$t('general.advancedSearch')"
          @click="filterDrawer = true"
        />
      </div>
      <div introjs="search">
        <pagination-search-bar class="search-bar mx-auto pt-6" />
        <pagination-chip-group class="tags-selection" :chips="TAGS" />
      </div>
      <div class="text-center pt-3 overline">
        {{ totalPrograms }} {{ $t("program.programsFound") }}
      </div>
      <v-row dense justify="space-between" class="cards-wrapper mx-auto py-3">
        <v-col
          cols="12"
          sm="6"
          lg="4"
          class="py-10"
          v-for="program in programsList"
          :key="program.id"
        >
          <info-card
            :img-url="program.logo"
            :title="program.name"
            :button-text="$tc('general.additionalInfo', 0)"
            :secondary-button-text="
              program.consumerJoinStatus === notJoinedText
                ? $t('userActions.join')
                : $t('userActions.leave')
            "
            @secondary-click="onJoinClick(program)"
            @click="openProgram(program)"
          >
            <template v-slot:subtitle>
              <span> {{ $t("general.status") }}: </span>
              <span
                :class="`${statusToColor[program.consumerJoinStatus]}--text`"
              >
                {{ statusToText[program.consumerJoinStatus] }}
              </span>
            </template>
            {{ program.description | trimText(36) }}
          </info-card>
        </v-col>
      </v-row>
    </div>
    <router-view v-model="isProgramOpen" />
    <end-of-page-detector @end-of-page="onEndOfPage" />
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex"
import debounce from "lodash/debounce"
import Api from "../../api"
import { SERVER, SEGMENT_EVENTS } from "../../helpers/constants/constants"
import InfoCard from "../../components/InfoCard"
import SideDrawer from "../../components/SideDrawer"
import PaginationSearchBar from "../../components/PaginationSearchBar"
import PaginationCheckboxGroup from "../../components/PaginationCheckboxGroup"
import PaginationChipGroup from "../../components/PaginationChipGroup"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import { PROGRAMS_CHECKBOX_FILTERS, TAGS } from "./constants"
import introjsSubscribeMixin from "../../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "ConsumerProgramsExplorer",
  components: {
    PaginationCheckboxGroup,
    PaginationChipGroup,
    InfoCard,
    SideDrawer,
    PaginationSearchBar,
    EndOfPageDetector,
  },
  mixins: [introjsSubscribeMixin],
  computed: {
    ...mapState("consumerProgram", ["programsList", "totalPrograms"]),
    ...mapGetters("school", ["schoolSlug"]),
  },

  methods: {
    ...mapActions("pagination", ["incrementPage", "updatePagination"]),
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

    openProgram(program) {
      this.isProgramOpen = true
      window.analytics.track(SEGMENT_EVENTS.programOpened, {
        program_slug: program.slug,
        program_name: program.name,
      })
      this.$router.push({
        name: "ConsumerProgramModal",
        params: { slug: program.slug },
      })
    },

    async getPrograms() {
      if (this.recentlyScrolled) {
        this.recentlyScrolled = false
        if (this.totalPrograms > this.programsList.length) {
          // add new programs if there are items left to fetch. do not override.
          this.getProgramsList({ override: false, usePagination: true })
        }
      } else {
        // fetch & override programs list
        this.updatePagination({ page: 1 })
        this.getProgramsList({ override: true, usePagination: true })
      }
    },

    onJoinClick: debounce(
      async function (program) {
        // (dis)request a program and change order status accordingly
        try {
          if (
            program.consumerJoinStatus ===
            SERVER.consumerProgramJoinStatus.notJoined
          ) {
            await this.joinProgram(program.slug)
            window.analytics.track(SEGMENT_EVENTS.programJoined, {
              program_slug: program.slug,
              program_name: program.name,
            })
            return this.showMessage(
              this.$t("success.joinRequestSentSuccessfully")
            )
          }
          if (
            program.consumerJoinStatus ===
            SERVER.consumerProgramJoinStatus.joined
          ) {
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
      500,
      { leading: true, trailing: false }
    ),
  },

  data() {
    return {
      notJoinedText: SERVER.consumerProgramJoinStatus.notJoined,
      PROGRAMS_CHECKBOX_FILTERS,
      TAGS,
      filterDrawer: false,
      recentlyScrolled: false,
      isProgramOpen: true,
      statusToText: {
        [SERVER.consumerProgramJoinStatus.pendingGroupAssignment]: this.$t(
          "program.pendingGroupAssignment"
        ),
        [SERVER.consumerProgramJoinStatus.joined]: this.$t(
          "program.inTheProgramAndAssignedToGroup"
        ),
        [SERVER.consumerProgramJoinStatus.notJoined]:
          this.$t("auth.notRegistered"),
      },
      statusToColor: {
        [SERVER.consumerProgramJoinStatus.pendingGroupAssignment]: "orange",
        [SERVER.consumerProgramJoinStatus.joined]: "success",
        [SERVER.consumerProgramJoinStatus.notJoined]: "",
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
.checkbox-group {
  float: right;
  width: 100%;
}
.checkbox-small::v-deep label {
  font-size: 12px;
}
.tags-selection,
.search-bar {
  max-width: 450px;
}
</style>
