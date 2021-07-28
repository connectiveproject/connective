import axios from "axios"
import { GET_EVENT_ORDERS_API_URL } from "../helpers/constants/constants"

const vendorEvent = {
  getEventOrders() {
    return axios.get(GET_EVENT_ORDERS_API_URL)
  },
}

export default vendorEvent
