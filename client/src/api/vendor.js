import axios from "axios"
import {
  GET_VENDOR_PROFILE_API_URL,
  UPDATE_VENDOR_PROFILE_API_URL,
} from "../helpers/constants/constants"

const vendor = {
  getProfile() {
    return axios.get(GET_VENDOR_PROFILE_API_URL)
  },

  updateProfile(slug, payload) {
    return axios.patch(`${UPDATE_VENDOR_PROFILE_API_URL}${slug}/`, payload)
  },
}

export default vendor
