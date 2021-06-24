import axios from "axios"
import {
  GET_INSTRUCTOR_EVENT_LIST_API_URL,
  GET_INSTRUCTOR_EVENT_API_URL,
  UPDATE_INSTRUCTOR_EVENT_API_URL,
} from "../helpers/constants/constants"

const instructorEvent = {
  getEvent(slug) {
    return axios.get(`${GET_INSTRUCTOR_EVENT_API_URL}${slug}/`)
  },
  updateEvent(slug, payload) {
    return axios.patch(`${UPDATE_INSTRUCTOR_EVENT_API_URL}${slug}/`, payload)
  },
  getEventList(params) {
    return axios.get(GET_INSTRUCTOR_EVENT_LIST_API_URL, { params })
  },
}

export default instructorEvent
