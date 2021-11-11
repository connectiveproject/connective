<template>
  <div :style="style">
    <navbar user-type="coordinator" />
    <router-view />
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
