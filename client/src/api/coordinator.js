import axios from "axios"
import {
  getCoordinatorProfileApiUrl,
  updateCoordinatorProfileApiUrl,
} from "../helpers/constants/constants"

const coordinator = {
  getProfile() {
    return axios.get(getCoordinatorProfileApiUrl)
  },

  updateProfile(slug, payload) {
    return axios.patch(`${updateCoordinatorProfileApiUrl}${slug}/`, payload)
  },
}

export default coordinator
