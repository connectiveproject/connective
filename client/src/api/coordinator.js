import axios from "axios"
import {
  getCoordinatorProfileApiUrl,
  updateCoordinatorProfileApiUrl,
} from "../helpers/constants/constants"

const coordinator = {
  getProfile() {
    return axios.get(getCoordinatorProfileApiUrl)
  },

  updateProfile(userId, payload) {
    return axios.put(`${updateCoordinatorProfileApiUrl}${userId}/`, payload)
  },
}

export default coordinator
