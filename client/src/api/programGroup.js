import axios from "axios"
import { GET_PROGRAM_GROUPS_API_URL } from "../helpers/constants/constants"

const programGroup = {
  getGroupList(params) {
    return axios.get(GET_PROGRAM_GROUPS_API_URL, { params })
  },
}

export default programGroup
