<template>
  <div>
    <v-row justify="center" v-for="post in posts" :key="post.slug" no-gutters>
      <v-col cols="11" md="5" lg="4">
        <post
          class="mx-auto"
          :author="post.authorName"
          :author-avatar="post.authorProfilePicture"
          :images="post.images"
          :content="post.postContent"
        />
      </v-col>
    </v-row>
  </div>
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
  async beforeRouteEnter(to, from, next) {
    const posts = await store.dispatch("instructorEvent/getFeedPosts")
    next(vm => (vm.posts = posts))
  },
  data() {
    return {
      posts: [],
    }
  },
}
</script>
