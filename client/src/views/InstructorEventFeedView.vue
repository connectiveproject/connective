<template>
  <div class="relative">
    <h1 v-text="$t('posts.myFeed')" class="mb-5" />
    <h2
      v-text="$t('posts.viewUpdatesAndPosts')"
      class="pb-12"
    />
    <v-row justify="center" v-for="post in posts" :key="post.slug" no-gutters>
      <v-col cols="11" md="5" lg="4">
        <post
          class="mx-auto"
          :author="post.authorName"
          :author-avatar="post.authorProfilePicture"
          :images="post.images"
          :content="post.postContent"
          :subtitle="post.creationTime"
        />
      </v-col>
    </v-row>
    <end-of-page-detector @endOfPage="onEndOfPage" />
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex"
import store from "../vuex/store"
import Post from "../components/Post"
import EndOfPageDetector from "../components/EndOfPageDetector"

export default {
  components: { Post, EndOfPageDetector },
  async beforeRouteEnter(to, from, next) {
    const posts = await store.dispatch("instructorEvent/getFeedPosts")
    next(vm => (vm.posts = posts))
  },
  methods: {
    ...mapActions("instructorEvent", ["getFeedPosts"]),
    ...mapActions("pagination", ["incrementPage"]),
    onEndOfPage() {
      this.incrementPage()
      if (this.totalFeedPosts > this.postList.length) {
        this.getFeedPosts(false)
      }
    },
  },
  data() {
    return {
      posts: [],
    }
  },
  computed: {
    ...mapState("instructorEvent", ["totalFeedPosts"]),
  },
}
</script>
