<template>
  <div :style="style">
    <navbar user-type="coordinator"/>
    <router-view/>
    <Post />
  </div>
</template>
<script>
import { BACKGROUNDS } from "../helpers/constants/images"
import Navbar from "../components/Navbar/Navbar"
import Post from "../components/posts/Post"

export default {
  components: {
    Navbar,
    Post,
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
