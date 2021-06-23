import axios from "axios"
import { GET_INSTRUCTOR_EVENTS_API_URL } from "../helpers/constants/constants"

const instructorEvent = {
  getEventList(params) {
    return axios.get(GET_INSTRUCTOR_EVENTS_API_URL, { params })
  },
}

export default instructorEvent
