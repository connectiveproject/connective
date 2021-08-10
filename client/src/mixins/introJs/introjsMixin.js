import EventBus from "../../helpers/eventBus"
import introJs from "intro.js"

export default {
  mounted() {
    EventBus.$on("startIntro", async () => {
      const configModule = await import("./config")
      const componentSteps = configModule.default[this.$options.name]
      if (componentSteps) {
        return introJs().setOptions({ steps: componentSteps }).start()
      }
      return introJs()
        .setOptions({ steps: configModule.default.noIntroMsg })
        .start()
    })
  },
  methods: {
    startIntro() {
      EventBus.$emit("startIntro")
    },
  },
}
