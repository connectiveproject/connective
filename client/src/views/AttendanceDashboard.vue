<template>
  <div>
    <h1 v-text="$t('attendanceDashboard.title')" class="mb-5" />

    <v-row justify="space-around">
      <v-col>
        <h2
          v-text="$t('attendanceDashboard.consumersInActivity')"
          class="pb-12"
        />
        <v-card>
          <bar-chart
            class="mx-auto my-10"
            :datasets="[{
              label: [$t('attendanceDashboard.consumersInActivityLabel')],
              data: [attendanceData.totalConsumers, attendanceData.inActivityConsumers],
              backgroundColor: ['#FFAEBCC0', '#A0E7E5C0'],
              borderWidth: 1,
            }]"
            :labels="attendanceLabels"
          />
        </v-card>
      </v-col>
      <v-col>
        <h2
          v-text="$t('attendanceDashboard.coursesInActivity')"
          class="pb-12"
        />
        <v-card>
          <bar-chart
            class="mx-auto my-10"
            :datasets="[{
              label: [$t('attendanceDashboard.coursesInActivityLabel')],
              data: [coursesInActivityData.totalCourses, coursesInActivityData.inActivityCourses],
              backgroundColor: ['#FFAEBCC0', '#A0E7E5C0'],
              borderWidth: 1,
            }]"
            :labels="coursesChartLabels"
          />
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapState } from "vuex"
import store from "../vuex/store"
import BarChart from "../components/Charts/BarChart"
export default {
  components: { BarChart },
  async beforeRouteEnter(to, from, next) {
    await store.dispatch("program/getConsumersInActivityStats")
    await store.dispatch("program/getCoursesInActivityStats")
    next()
  },
  data() {
    return {

    }
  },
  computed: {
    ...mapState("program", ["consumersInActivityStats", "coursesInActivityStats"]),
    attendanceLabels() {
      return ["כמות תלמידים", "כמות רשומים"]
    },
    attendanceData() {
      return this.consumersInActivityStats
    },
    coursesInActivityData() {
      return this.coursesInActivityStats
    },
    coursesChartLabels() {
      return ["קורסים", "קורסים פעילים"]
    }
  },
}
</script>
