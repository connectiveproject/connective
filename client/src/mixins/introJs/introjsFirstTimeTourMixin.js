import { mapActions, mapState } from "vuex"
import baseIntrojsMixin from "./baseIntrojsMixin"

export default {
  mixins: [baseIntrojsMixin],
  async mounted() {
    if (!this.userDetails.isSignupComplete) {
      this.startIntro()
      this.updateUserDetails({
        slug: this.userDetails.slug,
        userDetails: { isSignupComplete: true },
      })
    }
  },
  methods: {
    ...mapActions("user", ["updateUserDetails"]),
  },
  computed: {
    ...mapState("user", ["userDetails"]),
  },
}
