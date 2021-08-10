import introJs from "intro.js"
import Config from "./config"

export default {
  mounted() {
    const componentName = this.$options.name
    if (Config[componentName]) {
      introJs().setOptions({ steps: Config[componentName] }).start()
    }
  },
}
