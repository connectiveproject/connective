import axios from "axios"
import {
  GET_PROGRAMS_LIST_API_URL,
  GET_PROGRAM_MEDIA_LIST_API_URL,
  ORDER_SCHOOL_PROGRAM_API_URL,
  server,
} from "../helpers/constants/constants"

const program = {
  getProgram(slug) {
    return axios.get(`${GET_PROGRAMS_LIST_API_URL}${slug}/`)
  },
  getProgramMediaList(programSlug) {
    return axios.get(GET_PROGRAM_MEDIA_LIST_API_URL, { activity__slug: programSlug })
  },
  getProgramsList(params) {
    // :Object params: query params
    return axios.get(GET_PROGRAMS_LIST_API_URL, { params })
  },
  createProgramOrder(schoolSlug, programSlug) {
    return axios.post(ORDER_SCHOOL_PROGRAM_API_URL, {
      school: schoolSlug,
      activity: programSlug,
    })
  },
  cancelProgramOrder(schoolSlug, programSlug) {
    return axios.patch(`${ORDER_SCHOOL_PROGRAM_API_URL}${programSlug}/`, {
      status: server.programOrderStatus.cancelled,
      school: schoolSlug
    })
  },
  reCreateProgramOrder(schoolSlug, programSlug) {
    return axios.patch(`${ORDER_SCHOOL_PROGRAM_API_URL}${programSlug}/`, {
      status: server.programOrderStatus.pendingAdminApproval,
      school: schoolSlug
    })
  },
}

export default program
