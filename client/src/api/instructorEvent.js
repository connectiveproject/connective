import axios from "axios"
import {
  GET_INSTRUCTOR_EVENT_LIST_API_URL,
  GET_INSTRUCTOR_EVENT_API_URL,
  UPDATE_INSTRUCTOR_EVENT_API_URL,
} from "../helpers/constants/constants"

const instructorEvent = {
  getEvent(slug) {
    if (!slug) throw "getEvent: received empty slug"
    return axios.get(`${GET_INSTRUCTOR_EVENT_API_URL}${slug}/`)
  },
  updateEvent(slug, data) {
    if (!slug) throw "updateEvent: received empty slug"
    return axios.patch(`${UPDATE_INSTRUCTOR_EVENT_API_URL}${slug}/`, data)
  },
  getEventList(params) {
    return axios.get(GET_INSTRUCTOR_EVENT_LIST_API_URL, { params })
  },
}

export default instructorEvent
