import axios from "axios"
import {
  GET_USER_DETAILS_API_URL,
  UPDATE_USER_API_URL,
} from "../helpers/constants/constants"

const user = {
  getUserDetails() {
    // query for the user account details
    // return: axios Promise
    return axios.get(GET_USER_DETAILS_API_URL)
  },

  updateUserDetails(slug, data) {
    // update user account details using data
    // return: axios Promise
    return axios.patch(`${UPDATE_USER_API_URL}${slug}/`, data)
  },
}

export default user
