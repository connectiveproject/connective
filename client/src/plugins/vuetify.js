import Vue from "vue"
import Vuetify from "vuetify/lib/framework"
import Utils from "@/helpers/utils"

Vue.use(Vuetify)

export default new Vuetify({
  rtl: Utils.checkRtl(),
  theme: {
    themes: {
      light: {
        primary: "#10cb99",
        secondary: "#292929",
        "secondary-lighten-1": "#2d2c2c",
        "secondary-lighten-2": "#363535",
      },
    },
  },
})
