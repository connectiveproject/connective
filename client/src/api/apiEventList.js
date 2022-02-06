import axios from "axios"
import {
  GET_EVENT_LIST_API_URL,
  GET_EVENT_EXPORT_FILE_API_URL,
} from "@/helpers/constants/constants"

const apiEventList = {
  getEventList(params = {}) {
    return axios.get(GET_EVENT_LIST_API_URL, { params })
  },
  getPastEventsExportFile(params = {}) {
    // :Object params: query params
    return axios.get(GET_EVENT_EXPORT_FILE_API_URL, { params })
  },
}

export default apiEventList
