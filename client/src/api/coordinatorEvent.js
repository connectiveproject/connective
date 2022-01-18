import axios from "axios"
import {
  GET_COORDINATOR_EVENT_LIST_API_URL,
  GET_COORDINATOR_EVENT_EXPORT_FILE_API_URL,
} from "@/helpers/constants/constants"

const coordinatorEvent = {
  getEventList(params = {}) {
    return axios.get(GET_COORDINATOR_EVENT_LIST_API_URL, { params })
  },
  getPastEventsExportFile(params = {}) {
    // :Object params: query params
    return axios.get(GET_COORDINATOR_EVENT_EXPORT_FILE_API_URL, { params })
  },
}

export default coordinatorEvent
