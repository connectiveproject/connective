import { mapActions } from "vuex"
import baseIntrojsMixin from "./baseIntrojsMixin"

export default {
  mixins: [baseIntrojsMixin],
  mounted() {
    this.incrementSubscription()
    this.unsubscribeIntrojs = this.$store.subscribeAction(action => {
      if (action.type === "introjs/triggerIntro") {
        this.startIntro()
      }
    })
  },
  beforeDestroy() {
    this.decrementSubscription()
    this.unsubscribeIntrojs()
  },
  data() {
    return { unsubscribeIntrojs: null }
  },
  methods: {
    ...mapActions("introjs", [
      "incrementSubscription",
      "decrementSubscription",
    ]),
  },
}
