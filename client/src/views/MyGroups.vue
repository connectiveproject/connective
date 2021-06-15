<template>
  <div>
    <h1>hi</h1>
    <info-card
      v-for="group in groups"
      :starred="false"
      :key="group.id"
      :showStar="false"
      :title="group.name"
      :subtitle="group.activityName"
      :body="group.description"
      :imgUrl="group.activityLogo"
    >
      {{ group.description }}
      {{ group.consumers.length }}
    </info-card>
    <!-- add count of students & guide -->
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex"
import EndOfPageDetector from "../components/EndOfPageDetector"
import InfoCard from "../components/InfoCard"

export default {
  components: {
    EndOfPageDetector,
    InfoCard,
  },
  async mounted() {
    this.groups = await this.getGroupList()
  },
  computed: {
    ...mapState("programsGroups", ["totalGroups"]),
  },
  methods: {
    ...mapActions("pagination", ["incrementPage"]),
    ...mapActions("programsGroups", ["getGroupList"]),
    onEndOfPage() {
      this.incrementPage()
    },
    async fetchGroups() {
      if (this.groups.length < this.totalGroups) {
        this.groups = await this.getGroupList()
      }
    },
  },
  data() {
    return {
      groups: [],
    }
  },
  watch: {
    "$store.state.pagination": {
      // re-fetch if pagination changed
      deep: true,
      handler() {
        this.fetchGroups()
      },
    },
    groups: {
      deep: true,
      handler() {
        console.log(this.groups)
      },
    },
  },
}
</script>
