import axios from "axios"
import {
  getConsumerProfileApiUrl,
  updateConsumerProfileApiUrl,
} from "../helpers/constants/constants"

const consumer = {
  getProfile() {
    return axios.get(getConsumerProfileApiUrl)
  },

  updateProfile(slug, payload) {
    return axios.patch(`${updateConsumerProfileApiUrl}${slug}/`, payload)
  },
}

export default consumer
