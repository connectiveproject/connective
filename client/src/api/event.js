import axios from "axios"
import {
  GET_EVENT_LIST_API_URL,
  CREATE_EVENT_API_URL,
  CREATE_RECURRING_EVENTS_API_URL,
} from "../helpers/constants/constants"

const event = {
  getEventList(params) {
    return axios.get(GET_EVENT_LIST_API_URL, { params })
  },
  createEvent(data) {
    return axios.post(CREATE_EVENT_API_URL, data)
  },
  createRecurringEvents(data) {
    return axios.post(CREATE_RECURRING_EVENTS_API_URL, data)
  },
}

export default event
