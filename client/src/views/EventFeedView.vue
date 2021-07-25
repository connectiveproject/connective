<template>
  <v-col>
    <v-row
      align="center"
      justify="center"
      v-for="post in posts"
      :key="post.slug"
    >
      <Post :images="[{ url: post.imagesB64 }]" :content="post.postContent" />
    </v-row>
  </v-col>
</template>

<script>
import store from "../vuex/store"
import Post from "../components/posts/Post.vue"
import { mapActions } from "vuex"

export default {
  methods: {
    ...mapActions("instructorEvent", ["getFeedPosts"]),
  },
  components: { Post },
  data() {
    return {
      posts: [],
    }
  },
  async beforeRouteEnter(to, from, next) {
    // TODO GET
    const posts = await store.dispatch("instructorEvent/getFeedPosts")
    next(vm => (vm.posts = posts))
  },
}
</script>
