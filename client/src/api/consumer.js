import axios from "axios"
import {
  GET_CONSUMER_PROFILE_API_URL,
  UPDATE_CONSUMER_PROFILE_API_URL,
} from "../helpers/constants/constants"

const consumer = {
  getProfile() {
    return axios.get(GET_CONSUMER_PROFILE_API_URL)
  },

  updateProfile(slug, payload) {
    return axios.patch(`${UPDATE_CONSUMER_PROFILE_API_URL}${slug}/`, payload)
  },
}

export default consumer
