import axios from "axios"
import {
  getUserDetailsApiUrl,
  updateUserApiUrl,
} from "../helpers/constants/constants"

const user = {
  getUserDetails() {
    // query for the user account details
    // return: axios Promise
    return axios.get(getUserDetailsApiUrl)
  },

  updateUserDetails(username, payload) {
    // update user account details using payload
    // return: axios Promise
    return axios.put(`${updateUserApiUrl}${username}/`, payload)
  },
}

export default user
