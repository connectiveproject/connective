import axios from 'axios'
import { loginApiUrl, resetPasswordUrl } from '../helpers/constants/constants'

const auth = {
    login(email, password) {
        // params are string payloads login request
        // return: axios Promise
        return axios.post(loginApiUrl, { email, password })
    },

    resetPassword(uid, token, password, passwordConfirmation) {
        let url = `${resetPasswordUrl}${uid}/${token}/`
        let payload = {
            uid,
            token,
            new_password1: password,
            new_password2: passwordConfirmation,
        }
        return axios.post(url, payload)
    }
}

export default auth
