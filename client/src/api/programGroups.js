import axios from "axios"
import { GET_PROGRAMS_GROUPS_API_URL } from "../helpers/constants/constants"

const programGroups = {
  getGroupList(params) {
    return axios.get(GET_PROGRAMS_GROUPS_API_URL, { params })
  },
}

export default programGroups
