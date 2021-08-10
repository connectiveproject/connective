import EventBus from "../../helpers/eventBus"
import introJs from "intro.js"
import Config from "./config"

export default {
  mounted() {
    const componentName = this.$options.name
    EventBus.$on("startIntro", () => {
      if (Config[componentName]) {
        return introJs().setOptions({ steps: Config[componentName] }).start()
      }
      return introJs().setOptions({ steps: "noIntroMsg" }).start()
    })
  },
  methods: {
    startIntro() {
      EventBus.$emit("startIntro")
    },
  },
}
