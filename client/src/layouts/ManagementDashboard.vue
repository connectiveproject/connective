<template>
  <div :style="style">
    <navbar></navbar>
    <router-view></router-view>
  </div>
</template>
<script>
import { backgrounds } from "../helpers/constants/images"
import Navbar from "../components/Navbar"

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      style: {
        background: `url(${backgrounds.managementDashboard})`,
        "min-height": "100vh",
      },
    }
  },
}
</script>
