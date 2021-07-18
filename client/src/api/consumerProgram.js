import axios from "axios"
import {
  GET_CONSUMER_PROGRAM_LIST_API_URL,
  GET_PROGRAM_MEDIA_LIST_API_URL,
  CONSUMER_JOIN_PROGRAM_API_URL,
  CONSUMER_LEAVE_PROGRAM_API_URL,
} from "../helpers/constants/constants"

const consumerProgram = {
  getProgram(slug) {
    if (!slug) throw "getProgram: received empty slug"
    return axios.get(`${GET_CONSUMER_PROGRAM_LIST_API_URL}${slug}/`)
  },
  getProgramMediaList(programSlug) {
    if (!programSlug) throw "getProgramMediaList: received empty slug"
    return axios.get(GET_PROGRAM_MEDIA_LIST_API_URL, {
      params: {
        activity__slug: programSlug,
      },
    })
  },
  getProgramsList(params) {
    // :Object params: query params
    return axios.get(GET_CONSUMER_PROGRAM_LIST_API_URL, { params })
  },
  joinProgram(programSlug) {
    if (!programSlug) throw "joinProgram: received empty slug"
    const url = `${CONSUMER_JOIN_PROGRAM_API_URL}${programSlug}/join_group/`
    return axios.post(url, {})
  },
  leaveProgram(programSlug) {
    if (!programSlug) throw "leaveProgram: received empty slug"
    const url = `${CONSUMER_LEAVE_PROGRAM_API_URL}${programSlug}/leave_group/`
    return axios.post(url, {})
  },
}

export default consumerProgram
