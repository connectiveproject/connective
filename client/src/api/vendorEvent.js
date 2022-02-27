import axios from "axios"
import { GET_VENDOR_EVENT_ORDERS_API_URL, UPDATE_VENDOR_EVENT_ORDER_API_URL, GET_VENDOR_EVENT_LIST_API_URL } from "@/helpers/constants/constants"

const vendorEvent = {
  getEventOrders(params = {}) {
    return axios.get(GET_VENDOR_EVENT_ORDERS_API_URL, { params })
  },
  updateEventOrder(slug, data) {
    if (!slug) throw "updateEventOrder: received empty slug"
    return axios.patch(`${UPDATE_VENDOR_EVENT_ORDER_API_URL}${slug}/`, data)
  },
  getEventList(params = {}) {
    return axios.get(GET_VENDOR_EVENT_LIST_API_URL, { params })
  },
}

export default vendorEvent
