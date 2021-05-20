function get(cookieName) {
  // return the cookie value corresponding to cookieName, void if doesn't exist
  // :type cookieName: str
  // :rtype: str
  let allCookies = `; ${document.cookie}`
  let splitByName = allCookies.split(`; ${cookieName}=`)
  if (splitByName.length > 1) {
    return splitByName.pop().split(";").shift()
  }
}

function set(cookieName, cookieValue, days = undefined) {
  // set cookie value to cookie name, for a specified number of days
  // :type cookieName: str
  // :type cookieValue: str
  // :type days: int
  let expiryString = ""
  if (days) {
    let date = new Date()
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000)
    expiryString = `; expires=${date.toUTCString()}`
  }
  document.cookie = `${cookieName}=${cookieValue}${expiryString}; path=/`
}

function erase(cookieName) {
  // delete a cookie by changing expiry date
  // :type cookieName: str
  set(cookieName, "", -1)
}

const methods = { get, set, erase }
export default {
  // this is a local plugin
  install: function (Vue) {
    Vue.prototype.$cookies = methods
    Vue.$cookies = methods
  },
}
