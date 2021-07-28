import axios from "axios"
import { GET_VENDOR_EVENT_ORDERS_API_URL, UPDATE_VENDOR_EVENT_ORDER_API_URL } from "../helpers/constants/constants"

const vendorEvent = {
  getEventOrders() {
    return axios.get(GET_VENDOR_EVENT_ORDERS_API_URL)
  },
  updateEventOrder(slug, data) {
    console.log(data)
    if (!slug) throw "updateEventOrder: received empty slug"
    return axios.patch(`${UPDATE_VENDOR_EVENT_ORDER_API_URL}${slug}/`, data)
  },
}

export default vendorEvent
