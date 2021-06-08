import axios from "axios"
import {
  GET_COORDINATOR_PROFILE_API_URL,
  UPDATE_COORDINATOR_PROFILE_API_URL,
} from "../helpers/constants/constants"

const coordinator = {
  getProfile() {
    return axios.get(GET_COORDINATOR_PROFILE_API_URL)
  },

  updateProfile(slug, payload) {
    return axios.patch(`${UPDATE_COORDINATOR_PROFILE_API_URL}${slug}/`, payload)
  },
}

export default coordinator