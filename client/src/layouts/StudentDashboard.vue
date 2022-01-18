<template>
  <div>
    <navbar user-type="consumer" />
    <v-row no-gutters>
      <v-col class="mt-16 px-6 mx-auto" md="9" xl="8">
        <router-view />
      </v-col>
    </v-row>
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
