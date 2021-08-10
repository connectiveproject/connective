import { config, buttonLabels } from "./config"
import EventBus from "../../helpers/eventBus"
import introJs from "intro.js"

export default {
  mounted() {
    EventBus.$on("triggerIntro", this.startIntro)
  },
  methods: {
    triggerIntro() {
      EventBus.$emit("triggerIntro")
    },
    async startIntro() {
      if (config[this.$options.name]) {
        const componentSteps = this.componentconfigToSteps(
          config[this.$options.name]
        )
        return introJs()
          .setOptions({
            ...buttonLabels,
            steps: componentSteps,
          })
          .start()
      }
      return introJs()
        .setOptions({ ...buttonLabels, steps: config.noIntroMsg })
        .start()
    },
    componentconfigToSteps(config) {
      // return introJs format steps, based on selector
      return config.map(introObj => {
        if (!introObj.selector) {
          return introObj
        }
        return {
          ...introObj,
          element: document.querySelector(`[introjs="${introObj.selector}"]`),
        }
      })
    },
  },
}
