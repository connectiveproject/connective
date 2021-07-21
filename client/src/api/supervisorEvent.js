import axios from "axios"
import {
  GET_SUPERVISOR_EVENT_LIST_API_URL,
  GET_SUPERVISOR_EVENT_API_URL,
  CREATE_SUPERVISOR_EVENT_FEEDBACK_API_URL,
} from "../helpers/constants/constants"

const supervisorEvent = {
  getEvent(slug) {
    return axios.get(`${GET_SUPERVISOR_EVENT_API_URL}${slug}/`)
  },
  getEventList(params) {
    return axios.get(GET_SUPERVISOR_EVENT_LIST_API_URL, { params })
  },
  createEventFeedback(data) {
    return axios.post(CREATE_SUPERVISOR_EVENT_FEEDBACK_API_URL, data)
  },
}

export default supervisorEvent
