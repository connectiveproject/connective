import axios from "axios"
import { GET_CONSUMER_PROGRAM_GROUPS_API_URL } from "../helpers/constants/constants"

const consumerProgramGroup = {
  getGroupList(params = {}) {
    return axios.get(GET_CONSUMER_PROGRAM_GROUPS_API_URL, { params })
  },
}

export default consumerProgramGroup
