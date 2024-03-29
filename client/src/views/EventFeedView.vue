<template>
  <div class="relative px-3 mt-8 px-lg-16 mx-lg-16 mt-lg-16">
    <h1 v-text="$t('posts.myFeed')" class="mb-5" />
    <h2 v-text="$t('posts.viewUpdatesAndPostsInRealTime!')" class="pb-12" />
    <v-row justify="center" v-for="post in posts" :key="post.slug" no-gutters>
      <v-col cols="12" md="5" lg="4">
        <post
          class="mx-auto"
          :author="post.authorName"
          :author-avatar="post.authorProfilePicture"
          :images="post.images.map(img => img.imageUrl)"
          :content="post.postContent"
          :subtitle="ApiStringToReadableDate(post.created)"
        />
      </v-col>
    </v-row>
    <div v-if="!posts.length" class="text-center overline">
      0 {{ $t("posts.postsFound") }}
    </div>
    <end-of-page-detector @end-of-page="onEndOfPage" />
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex"
import store from "@/vuex/store"
import Utils from "../helpers/utils"
import Post from "../components/Post"
import EndOfPageDetector from "../components/EndOfPageDetector"
import introjsSubscribeMixin from "../mixins/introJs/introjsSubscribeMixin"

export default {
  name: "EventFeedView",
  components: { Post, EndOfPageDetector },
  mixins: [introjsSubscribeMixin],
  async beforeRouteEnter(to, from, next) {
    const posts = await store.dispatch("eventFeedPost/getFeedPosts", {
      override: true,
      usePagination: true,
    })
    next(vm => (vm.posts = posts))
  },
  methods: {
    ...mapActions("eventFeedPost", ["getFeedPosts"]),
    ...mapActions("pagination", ["incrementPage"]),
    ApiStringToReadableDate: Utils.ApiStringToReadableDate,
    onEndOfPage() {
      this.incrementPage()
      if (this.totalFeedPosts > this.posts.length) {
        this.getFeedPosts({ override: false, usePagination: true })
      }
    },
  },
  data() {
    return {
      posts: [],
    }
  },
  computed: {
    ...mapState("eventFeedPost", ["totalFeedPosts"]),
  },
}
</script>
