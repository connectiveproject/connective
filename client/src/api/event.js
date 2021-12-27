import axios from "axios"
import {
  GET_EVENT_LIST_API_URL,
  CREATE_EVENT_ORDER_API_URL,
  GET_EVENT_ORDERS_API_URL,
  DELETE_EVENT_ORDER_API_URL,
  DELETE_EVENT_API_URL,
} from "../helpers/constants/constants"

const event = {
  getEventList(params = {}) {
    return axios.get(GET_EVENT_LIST_API_URL, { params })
  },
  createEventOrder(data) {
    return axios.post(CREATE_EVENT_ORDER_API_URL, data)
  },
  getEventOrders(params = {}) {
    return axios.get(GET_EVENT_ORDERS_API_URL, { params })
  },
  deleteEventOrder(slug) {
    if (!slug) throw "deleteEventOrder: received empty slug"
    return axios.delete(`${DELETE_EVENT_ORDER_API_URL}${slug}/`)
  },
  deleteEvent(slug) {
    if (!slug) throw "deleteEvent: received empty slug"
    return axios.delete(`${DELETE_EVENT_API_URL}${slug}/`)
  }
}

export default event
