import axios from "axios"
import {
  GET_MY_NOTIFICATIONS,
  GET_HAS_NEW_NOTIFICATIONS,
} from "@/helpers/constants/constants"

const vendor = {
  getNotificationList() {
    return axios.get(GET_MY_NOTIFICATIONS)
  },

  hasNew() {
    return axios.get(`${GET_HAS_NEW_NOTIFICATIONS}`)
  },

  // TODO implement
  markAllAsRead(latestSlug) {
    if (!latestSlug) throw "markAllAsRead: received empty slug"
    return axios.patch("TODO implement")
  },
}

export default vendor
