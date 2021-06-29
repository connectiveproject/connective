import axios from "axios"
import { GET_PROGRAM_GROUPS_API_URL, CREATE_PROGRAM_GROUP_API_URL } from "../helpers/constants/constants"

const programGroup = {
  getGroupList(params) {
    return axios.get(GET_PROGRAM_GROUPS_API_URL, { params })
  },
  createGroup(payload) {
    return axios.post(CREATE_PROGRAM_GROUP_API_URL, payload)
  }
}

export default programGroup
