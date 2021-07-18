import axios from "axios"
import {
  GET_COORDINATOR_PROFILE_API_URL,
  UPDATE_COORDINATOR_PROFILE_API_URL,
} from "../helpers/constants/constants"

const coordinator = {
  getProfile() {
    return axios.get(GET_COORDINATOR_PROFILE_API_URL)
  },

  updateProfile(slug, data) {
    if (!slug) throw "updateProfile: received empty slug"
    return axios.patch(`${UPDATE_COORDINATOR_PROFILE_API_URL}${slug}/`, data)
  },
}

export default coordinator
