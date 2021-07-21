import axios from "axios"
import {
  GET_SUPERVISOR_PROGRAM_LIST_API_URL,
  GET_PROGRAM_MEDIA_LIST_API_URL,
  SUPERVISOR_JOIN_PROGRAM_API_URL,
  SUPERVISOR_LEAVE_PROGRAM_API_URL,
} from "../helpers/constants/constants"

const supervisorProgram = {
  getProgram(slug) {
    return axios.get(`${GET_SUPERVISOR_PROGRAM_LIST_API_URL}${slug}/`)
  },
  getProgramMediaList(programSlug) {
    return axios.get(GET_PROGRAM_MEDIA_LIST_API_URL, {
      params: {
        activity__slug: programSlug,
      },
    })
  },
  getProgramsList(params) {
    // :Object params: query params
    return axios.get(GET_SUPERVISOR_PROGRAM_LIST_API_URL, { params })
  },
  joinProgram(programSlug) {
    const url = `${SUPERVISOR_JOIN_PROGRAM_API_URL}${programSlug}/join_group/`
    return axios.post(url, {})
  },
  leaveProgram(programSlug) {
    const url = `${SUPERVISOR_LEAVE_PROGRAM_API_URL}${programSlug}/leave_group/`
    return axios.post(url, {})
  },
}

export default supervisorProgram
