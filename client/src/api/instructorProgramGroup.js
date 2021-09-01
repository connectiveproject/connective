import axios from "axios"
import { GET_INSTRUCTOR_PROGRAM_GROUP_CONSUMERS_API_URL } from "../helpers/constants/constants"

const instructorProgramGroup = {
  getConsumers(groupSlugs) {
    if (!groupSlugs) throw "getConsumers: received empty slug"
    return axios.get(GET_INSTRUCTOR_PROGRAM_GROUP_CONSUMERS_API_URL, {
      params: { slugs: groupSlugs.join(",") },
    })
  },
}

export default instructorProgramGroup
