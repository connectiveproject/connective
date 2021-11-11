<template>
  <div>
    <navbar user-type="instructor" />
    <router-view />
  </div>
</template>
<script>
import Navbar from "@/components/Navbar/Navbar"
import introjsFirstTimeTourMixin from "../mixins/introJs/introjsFirstTimeTourMixin"

export default {
  name: "InstructorDashboard",
  components: { Navbar },
  mixins: [introjsFirstTimeTourMixin],
}
</script>
