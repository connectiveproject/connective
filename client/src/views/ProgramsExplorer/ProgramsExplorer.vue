<template>
  <div>
    <v-row class="pt-10 ml-0">
      <v-col
        v-if="!isConsumer"
        cols="4"
        md="3"
        class="right-pane white-bg"
        :class="{ 'pr-10': !$vuetify.breakpoint.mobile }"
      >
        <pagination-checkbox-group
          v-for="filter in PROGRAMS_CHECKBOX_FILTERS"
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
        :class="{ 'px-10': !$vuetify.breakpoint.mobile, 'mx-auto': isConsumer }"
      >
        <h1 v-text="$t('program.programsExplorer')" class="pb-6" />
        <h3 v-text="getSubtitle(isConsumer)" />
        <pagination-search-bar class="search-bar mx-auto pt-16" />
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
              v-model="program.isOrdered"
              :imgUrl="program.logo"
              :title="program.name"
              :body="program.description"
              :subtitle="getCardSubtitle(program.orderStatus)"
              @input="e => onStarChange(program, e)"
              @click="openProgram(program.slug)"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <router-view v-model="isProgramOpen" />
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>

<script>
import InfoCard from "../../components/InfoCard"
import PaginationCheckboxGroup from "../../components/PaginationCheckboxGroup"
import PaginationSearchBar from "../../components/PaginationSearchBar"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import {
  PROGRAMS_CHECKBOX_FILTERS,
  SERVER,
} from "../../helpers/constants/constants"
import { mapActions, mapGetters, mapState } from "vuex"
import { getSubtitle } from "./helpers"

export default {
  components: {
    InfoCard,
    PaginationCheckboxGroup,
    PaginationSearchBar,
    EndOfPageDetector,
  },

  computed: {
    ...mapState("program", ["programsList", "totalPrograms"]),
    ...mapGetters("user", ["isConsumer"]),
    ...mapGetters("school", ["schoolSlug"]),
  },

  methods: {
    ...mapActions("pagination", ["incrementPage", "updatePagination"]),
    ...mapActions("program", [
      "getProgramsList",
      "createProgramOrder",
      "cancelProgramOrder",
      "reCreateProgramOrder",
    ]),
    getSubtitle,

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
        // fetch & ovrride programs list
        this.updatePagination({ page: 1 })
        this.getProgramsList(true)
      }
    },

    getCardSubtitle(orderStatus) {
      const prefix = this.$t("general.status")
      let status = this.$t("program.available")
      if (orderStatus) {
        status = this.$t(`program.${orderStatus}`)
      }
      return `${prefix}: ${status}`
    },

    onStarChange(program, isStarred) {
      // (dis)request a program and change order status accordingly
      try {
        if (isStarred) {
          this.requestProgram(program)
        } else {
          this.disRequestProgram(program)
        }
      } catch (err) {
        // add toast
        return
      }
    },

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
      recentlyScrolled: false,
      isProgramOpen: true,
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
.search-bar {
  max-width: 450px;
}
</style>
