/*
steps to adding introjs to example.vue file:
1. add "name" attribute & this mixin to the example.vue
2. add introjs attributes to elements in example.vue (e.g., <div introjs="example-attr"></div> )
3. add the introjs attribute value to ./config file
*/
import introJs from "intro.js"
import { config, buttonLabels } from "./config"

export default {
  methods: {
    startIntro() {
      if (config[this.$options.name]) {
        const componentSteps = this.componentConfigToSteps(
          config[this.$options.name]()
        )
        const intro = introJs().setOptions({
          ...buttonLabels(),
          showProgress: true,
          showBullets: false,
          steps: componentSteps,
        })
        intro.onbeforechange(function () {
          const action = this._introItems[this._currentStep].preStepAction
          if (action) {
            action()
          }
        })
        return intro.start()
      }
      return introJs()
        .setOptions({ ...buttonLabels(), steps: config.noIntroMsg })
        .start()
    },
    componentConfigToSteps(config) {
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
