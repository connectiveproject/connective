import axios from "axios"
import {
  GET_CONSUMER_EVENT_LIST_API_URL,
  GET_CONSUMER_EVENT_API_URL,
  CREATE_CONSUMER_EVENT_FEEDBACK_API_URL,
} from "../helpers/constants/constants"

const consumerEvent = {
  getEvent(slug) {
    return axios.get(`${GET_CONSUMER_EVENT_API_URL}${slug}/`)
  },
  getEventList(params) {
    return axios.get(GET_CONSUMER_EVENT_LIST_API_URL, { params })
  },
  createEventFeedback(data) {
    return axios.post(CREATE_CONSUMER_EVENT_FEEDBACK_API_URL, data)
  },
}

export default consumerEvent
