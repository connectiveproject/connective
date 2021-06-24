import axios from "axios"
import { GET_CONSUMER_EVENT_LIST_API_URL } from "../helpers/constants/constants"

const consumerEvent = {
  getEventList(params) {
    return axios.get(GET_CONSUMER_EVENT_LIST_API_URL, { params })
  },
}

export default consumerEvent
