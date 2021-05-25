import axios from "axios"
import {
  getUserDetailsApiUrl,
  getProfileApiUrl,
  updateProfileApiUrl,
  updateUserApiUrl,
} from "../helpers/constants/constants"

const user = {
  getProfile() {
    // query for the user profile
    // return: axios Promise
    return axios.get(getProfileApiUrl)
  },

  updateProfile(slug, payload) {
    // put user profile information
    // return: axios Promise
    return axios.put(`${updateProfileApiUrl}${slug}/`, payload)
  },

  getUserDetails() {
    // query for the user account details
    // return: axios Promise
    return axios.get(getUserDetailsApiUrl)
  },

  updateUserDetails(slug, payload) {
    // update user account details using payload
    // return: axios Promise
    return axios.put(`${updateUserApiUrl}${slug}/`, payload)
  },
}

export default user
