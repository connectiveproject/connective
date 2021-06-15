import Vue from "vue"

Vue.filter("trimText", (str, maxLength) => {
  if (str.length > maxLength) {
    return str.substring(0, maxLength) + "...."
  }
  return str
})
