import axios from "axios"
import { GET_SUPERVISOR_PROGRAM_GROUPS_API_URL } from "../helpers/constants/constants"

const supervisorProgramGroup = {
  getGroupList(params) {
    return axios.get(GET_SUPERVISOR_PROGRAM_GROUPS_API_URL, { params })
  },
}

export default supervisorProgramGroup
