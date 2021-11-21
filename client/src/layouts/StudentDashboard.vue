<template>
  <div>
    <navbar user-type="consumer" />
    <router-view />
  </div>
</template>
<script>
import Navbar from "@/components/Navbar/Navbar"
import introjsFirstTimeTourMixin from "../mixins/introJs/introjsFirstTimeTourMixin"

export default {
  name: "StudentDashboard",
  components: { Navbar },
  mixins: [introjsFirstTimeTourMixin],
}
</script>
