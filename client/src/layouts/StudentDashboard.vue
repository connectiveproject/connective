<template>
  <div>
    <navbar user-type="consumer"/>
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
