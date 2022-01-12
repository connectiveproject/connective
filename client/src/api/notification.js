import axios from "axios"
import {
  GET_MY_NOTIFICATIONS,
  GET_HAS_NEW_NOTIFICATIONS,
  UPDATE_NOTIFICATION,
  UPDATE_NOTIFICATIONS_MARK_ALL_AS_READ,

} from "@/helpers/constants/constants"

const notification = {
  getNotificationList() {
    const params = { page_size: 20 }
    return axios.get(GET_MY_NOTIFICATIONS, { params })
  },

  hasNew() {
    return axios.get(GET_HAS_NEW_NOTIFICATIONS)
  },

  dismissNotification(slug) {
    if (!slug) throw "dismissNotification: received empty slug"
    return axios.patch(`${UPDATE_NOTIFICATION}${slug}/`, { status: "DISMISSED" })
  },

  markAllAsRead(maxSlug) {
    if (!maxSlug) throw "markAllAsRead: received empty slug"
    return axios.post(UPDATE_NOTIFICATIONS_MARK_ALL_AS_READ, { maxSlug: maxSlug })
  },
}

export default notification
