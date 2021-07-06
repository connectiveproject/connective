<template>
  <div>
    <navbar userType="vendor"/>
    <router-view/>
  </div>
</template>
<script>
import Navbar from "../components/Navbar/Navbar"

export default {
  components: {
    Navbar,
  },
}
</script>
