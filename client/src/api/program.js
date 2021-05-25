import axios from "axios"
import {
  getProgramsListApiUrl,
  getProgramMediaListApiUrl,
} from "../helpers/constants/constants"

const program = {
  getProgram(slug) {
    return axios.get(getProgramsListApiUrl + slug)
  },
  getProgramMediaList(programSlug) {
    return axios.get(getProgramMediaListApiUrl, { activity__slug: programSlug })
  },
  getProgramsList(params) {
    // :Object params: query params
    return axios.get(getProgramsListApiUrl, { params })
  },
}

export default program
