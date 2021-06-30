import axios from "axios"
import { GET_INSTRUCTOR_PROGRAM_GROUP_CONSUMERS_API_URL } from "../helpers/constants/constants"

const instructorProgramGroup = {
  getConsumers(groupSlug) {
    return axios.get(`${GET_INSTRUCTOR_PROGRAM_GROUP_CONSUMERS_API_URL}${groupSlug}/group_consumers/`)
  },
}

export default instructorProgramGroup
