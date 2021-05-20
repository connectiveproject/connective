import Vue from "vue"
import VueI18n from "vue-i18n"

Vue.use(VueI18n)

function loadLocaleMessages() {
  // return an object containing translations from specified locale JSON files
  const fileNames = ["he"]
  let messages = {}
  for (let name of fileNames) {
    messages[name] = require(`../locales/${name}.json`)
  }
  return messages
}

export default new VueI18n({
  locale: "he",
  fallbackLocale: "he",
  messages: loadLocaleMessages(),
})
