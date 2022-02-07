<template>
  <div :style="style">
    <navbar user-type="coordinator" />
    <v-row no-gutters>
      <v-col class="mt-16 px-6 mx-auto" md="9" xl="8">
        <router-view />
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { BACKGROUNDS } from "../helpers/constants/images"
import Navbar from "@/components/Navbar/Navbar"
import introjsFirstTimeTourMixin from "../mixins/introJs/introjsFirstTimeTourMixin"

export default {
  name: "CoordinatorDashboard",
  components: { Navbar },
  mixins: [introjsFirstTimeTourMixin],
  data() {
    return {
      style: {
        background: `url(${BACKGROUNDS.managementDashboard})`,
        "min-height": "100vh",
      },
    }
  },
}
</script>
