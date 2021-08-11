/*
steps to adding introjs to example.vue file:
1. add "name" attribute & this mixin to the example.vue
2. add introjs attributes to elements in example.vue (e.g., <div introjs="example-attr"></div> )
3. add the introjs attribute value to ./config file
*/
import introJs from "intro.js"
import { mapActions } from "vuex"
import { config, buttonLabels } from "./config"

export default {
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
