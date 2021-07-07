import Vue from "vue"

export function trimText(str, maxLength) {
  if (str.length > maxLength) {
    return str.substring(0, maxLength) + "...."
  }
  return str
}

Vue.filter("trimText", trimText)
