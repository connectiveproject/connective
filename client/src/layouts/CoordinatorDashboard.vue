<template>
  <div :style="style">
    <coordinator-navbar user-type="coordinator"/>
    <router-view/>
  </div>
</template>
<script>
import { BACKGROUNDS } from "../helpers/constants/images"
import CoordinatorNavbar from "../components/Navbar/CoordinatorNavbar"

export default {
  components: {
    CoordinatorNavbar,
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
