import Vue from "vue"
import Vuetify from "vuetify"
import VueI18n from "vue-i18n"
import i18n from "../src/plugins/i18n.js"
import "../src/helpers/validators"
import "!style-loader!css-loader!sass-loader!../src/styles/main.scss"
import "./vuetify"
import "../src/filters"

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
}

Vue.use(Vuetify)
Vue.use(VueI18n)
const vuetify = new Vuetify()

export const decorators = [
  (story, context) => {
    // wrap the passed component within the passed context
    const wrapped = story(context)
    // extend Vue to use Vuetify around the wrapped component
    return Vue.extend({
      vuetify,
      i18n,
      components: { wrapped },
      props: {
        locale: {
          type: String,
          default: "he",
        },
      },
      watch: {
        dark: {
          immediate: true,
          handler(val) {
            this.$vuetify.theme.dark = val
          },
        },
        locale: {
          immediate: true,
          handler(val) {
            this.$i18n.locale = val
          },
        },
      },
      template: `
        <v-app>
          <v-container fluid>
            <wrapped />
          </v-container>
        </v-app>
      `,
    })
  },
]
