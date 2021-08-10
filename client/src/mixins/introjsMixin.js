import EventBus from "../helpers/eventBus"
import introJs from "intro.js"

export default {
  mounted() {
    EventBus.$on("startIntro", () => introJs().start())
  },
}
