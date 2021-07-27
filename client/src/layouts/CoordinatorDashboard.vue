<template>
  <div :style="style">
    <navbar user-type="coordinator"/>
    <router-view/>
  </div>
</template>
<script>
import { BACKGROUNDS } from "../helpers/constants/images"
import Navbar from "../components/Navbar/Navbar"

export default {
  components: {
    Navbar,
  },
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
