import axios from "axios"
import { GET_EVENT_LIST_API_URL } from "../helpers/constants/constants"

const event = {
  getEventList(params) {
    return axios.get(GET_EVENT_LIST_API_URL, { params })
  },
}

export default event
