import axios from "axios"
import { LOGIN_API_URL, RESET_PASSWORD_URL } from "../helpers/constants/constants"

const auth = {
  login(email, password) {
    // params are strings for login request
    // return: axios Promise
    return axios.post(LOGIN_API_URL, { email, password })
  },

  resetPassword(uid, token, password, passwordConfirmation) {
    let url = `${RESET_PASSWORD_URL}${uid}/${token}/`
    let data = {
      uid,
      token,
      new_password1: password,
      new_password2: passwordConfirmation,
    }
    return axios.post(url, data)
  },
}

export default auth
