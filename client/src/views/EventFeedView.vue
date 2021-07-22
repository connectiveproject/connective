<template>
  <div>
    <v-row v-for="post in posts" :key="post.slug">
      <Post />
    </v-row>
  </div>
</template>

<script>
// import store from "../vuex/store"
import Post from "../components/posts/Post.vue"
export default {
  components: { Post },
  data() {
    return {
      posts: [],
    }
  },
  async beforeRouteEnter(to, from, next) {
    // TODO GET
    // await store.dispatch("instructorEvent/getPastEvents", { daysAgo: 60, unsummarizedOnly: true })
    next()
  },
}
</script>
