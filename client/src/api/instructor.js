import axios from "axios"
import {
  GET_INSTRUCTOR_PROFILE_API_URL,
  UPDATE_INSTRUCTOR_PROFILE_API_URL,
} from "../helpers/constants/constants"

const instructor = {
  getProfile() {
    return axios.get(GET_INSTRUCTOR_PROFILE_API_URL)
  },

  updateProfile(slug, data) {
    if (!slug) return console.error("updateProfile: received empty slug")
    return axios.patch(`${UPDATE_INSTRUCTOR_PROFILE_API_URL}${slug}/`, data)
  },
}

export default instructor
