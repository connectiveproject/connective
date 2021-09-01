import axios from "axios"
import {
  GET_SUPERVISOR_PROFILE_API_URL,
  UPDATE_SUPERVISOR_PROFILE_API_URL,
} from "@/helpers/constants/constants"

const supervisor = {
  getProfile() {
    return axios.get(GET_SUPERVISOR_PROFILE_API_URL)
  },

  updateProfile(slug, data) {
    if (!slug) throw "updateProfile: received empty slug"
    return axios.patch(`${UPDATE_SUPERVISOR_PROFILE_API_URL}${slug}/`, data)
  },
}

export default supervisor
