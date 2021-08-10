<template>
  <div>
    <v-navigation-drawer temporary right v-model="filterDrawer" fixed>
      <pagination-checkbox-group
        v-for="filter in PROGRAMS_CHECKBOX_FILTERS"
        :key="filter.id"
        :name="filter.name"
        :title="filter.readableName"
        :items="filter.options"
        class="checkbox-group"
        :class="{ 'checkbox-small': $vuetify.breakpoint.mobile }"
      />
    </v-navigation-drawer>
    <div class="ma-3 pa-3 px-lg-16 mx-lg-16 py-lg-6 my-lg-6">
      <div class="d-flex justify-space-between flex-wrap">
        <div class="pb-7">
          <h1 v-text="$t('program.programsExplorer')" class="pb-6" />
          <h3
            v-text="
              $t(
                'program.findForProgramsThatFitTheSchoolPedagogicalApproachAndStartCollaborating!'
              )
            "
          />
        </div>
        <v-btn
          class="mx-auto mx-md-0 primary"
          @click="filterDrawer = true"
          v-text="$t('general.advancedSearch')"
        />
      </div>
      <pagination-search-bar class="search-bar mx-auto pt-16" />
      <pagination-chip-group class="tags-selection" :chips="TAGS" />
      <div class="text-center pt-10 overline">
        {{ totalPrograms }} {{ $t("program.programsFound") }}
      </div>
      <v-row dense justify="space-between" class="cards-wrapper mx-auto py-10">
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
            :button-text="$t('program.forProgramDetails')"
            @click="openProgram(program.slug)"
            :secondary-button-text="
              program.isOrdered
                ? $t('userActions.leave')
                : $t('userActions.join')
            "
            @secondary-click="onOrderClick(program)"
          >
            <template v-slot:subtitle>
              <span> {{ $t("general.status") }}: </span>
              <span :class="`${statusToColor[program.orderStatus]}--text`">
                {{ statusToText[program.orderStatus] }}
              </span>
            </template>
            {{ program.description | trimText(70) }}
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
import InfoCard from "../../components/InfoCard"
import PaginationCheckboxGroup from "../../components/PaginationCheckboxGroup"
import PaginationSearchBar from "../../components/PaginationSearchBar"
import PaginationChipGroup from "../../components/PaginationChipGroup"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import { SERVER } from "../../helpers/constants/constants"
import { PROGRAMS_CHECKBOX_FILTERS, TAGS } from "./constants"

export default {
  components: {
    InfoCard,
    PaginationCheckboxGroup,
    PaginationSearchBar,
    PaginationChipGroup,
    EndOfPageDetector,
  },

  computed: {
    ...mapState("program", ["programsList", "totalPrograms"]),
    ...mapGetters("school", ["schoolSlug"]),
  },

  methods: {
    ...mapActions("snackbar", ["showMessage"]),
    ...mapActions("pagination", ["incrementPage", "updatePagination"]),
    ...mapActions("program", [
      "getProgramsList",
      "createProgramOrder",
      "cancelProgramOrder",
      "reCreateProgramOrder",
    ]),

    onEndOfPage() {
      // trigger programs load on end of page
      this.recentlyScrolled = true
      this.incrementPage()
    },

    openProgram(slug) {
      this.isProgramOpen = true
      this.$router.push({ name: "ProgramModal", params: { slug } })
    },

    async getPrograms() {
      if (this.recentlyScrolled) {
        this.recentlyScrolled = false
        if (this.totalPrograms > this.programsList.length) {
          // add new programs if there are items left to fetch. do not override.
          this.getProgramsList(false)
        }
      } else {
        // fetch & override programs list
        this.updatePagination({ page: 1 })
        this.getProgramsList(true)
      }
    },

    onOrderClick: debounce(
      async function (program) {
        // (dis)request a program and change order status accordingly
        try {
          if (program.isOrdered) {
            await this.disRequestProgram(program)
            this.showMessage(this.$t("success.programParticipationCancelled"))
          } else {
            await this.requestProgram(program)
            this.showMessage(
              this.$t("success.joinRequestSentAndIsWaitingForAdminApproval")
            )
          }
        } catch (err) {
          this.showMessage(Api.utils.parseResponseError(err))
        }
      },
      500,
      { leading: true, trailing: false }
    ),

    requestProgram(program) {
      if (program.orderStatus === SERVER.programOrderStatus.cancelled) {
        return this.reCreateProgramOrder({
          schoolSlug: this.schoolSlug,
          programSlug: program.slug,
        })
      }
      return this.createProgramOrder({
        schoolSlug: this.schoolSlug,
        programSlug: program.slug,
      })
    },

    disRequestProgram(program) {
      return this.cancelProgramOrder({
        schoolSlug: this.schoolSlug,
        programSlug: program.slug,
      })
    },
  },

  data() {
    return {
      PROGRAMS_CHECKBOX_FILTERS,
      TAGS,
      filterDrawer: false,
      recentlyScrolled: false,
      isProgramOpen: true,
      statusToText: {
        [SERVER.programOrderStatus.cancelled]: this.$t(
          "program.requestCancelled"
        ),
        [SERVER.programOrderStatus.approved]: this.$t(
          "program.requestApproved"
        ),
        [SERVER.programOrderStatus.pendingAdminApproval]: this.$t(
          "program.pendingAdminApproval"
        ),
        [SERVER.programOrderStatus.notOrdered]: this.$t("program.available"),
      },
      statusToColor: {
        [SERVER.programOrderStatus.cancelled]: "error",
        [SERVER.programOrderStatus.approved]: "success",
        [SERVER.programOrderStatus.pendingAdminApproval]: "orange",
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
        this.$router.push({ name: "ProgramsExplorer" })
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
