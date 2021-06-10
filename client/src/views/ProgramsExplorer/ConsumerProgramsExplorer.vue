<template>
  <div>
    <v-row class="pt-10 ml-0">
      <v-col
        cols="8"
        md="9"
        :class="{ 'px-10': !$vuetify.breakpoint.mobile }"
        class="mx-auto"
      >
        <h1 v-text="$t('program.programsExplorer')" class="pb-6" />
        <h3 v-text="$t('program.searchAndFindTheProgramsYouLike!')" />
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
              v-model="program.isConsumerJoined"
              :imgUrl="program.logo"
              :title="program.name"
              :body="program.description"
              :subtitle="getCardSubtitle(program.isConsumerJoined)"
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
import PaginationSearchBar from "../../components/PaginationSearchBar"
import EndOfPageDetector from "../../components/EndOfPageDetector"
import { mapActions, mapGetters, mapState } from "vuex"

export default {
  components: {
    InfoCard,
    PaginationSearchBar,
    EndOfPageDetector,
  },

  computed: {
    ...mapState("consumerProgram", ["programsList", "totalPrograms"]),
    ...mapGetters("school", ["schoolSlug"]),
  },

  methods: {
    ...mapActions("pagination", ["incrementPage", "updatePagination"]),
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

    getCardSubtitle(isConsumerJoined) {
      const prefix = this.$t("general.status")
      let status = this.$t("auth.notRegistered")
      if (isConsumerJoined) {
        status = this.$t("auth.registered")
      }
      return `${prefix}: ${status}`
    },

    onStarChange(program, isStarred) {
      // (dis)request a program and change order status accordingly
      try {
        if (isStarred) {
          this.joinProgram(program.slug)
        } else {
          this.leaveProgram(program.slug)
        }
      } catch (err) {
        // add toast
        console.warn(err)
      }
    },
  },

  data() {
    return {
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
  max-width: 450px;
}
</style>
