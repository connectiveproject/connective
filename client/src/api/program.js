import axios from "axios"
import {
  getProgramsListApiUrl,
  getProgramMediaListApiUrl,
  orderSchoolProgramApiUrl,
  server,
} from "../helpers/constants/constants"

const program = {
  getProgram(slug) {
    return axios.get(`${getProgramsListApiUrl}${slug}/`)
  },
  getProgramMediaList(programSlug) {
    return axios.get(getProgramMediaListApiUrl, { activity__slug: programSlug })
  },
  getProgramsList(params) {
    // :Object params: query params
    return axios.get(getProgramsListApiUrl, { params })
  },
  orderProgram(schoolSlug, programSlug) {
    return axios.post(orderSchoolProgramApiUrl, {
      school: schoolSlug,
      activity: programSlug,
    })
  },
  disOrderProgram(schoolSlug, programSlug) {
    return axios.patch(`${orderSchoolProgramApiUrl}${programSlug}/`, {
      status: server.programOrderStatus.cancelled,
      school: schoolSlug
    })
  },
  reOrderProgram(schoolSlug, programSlug) {
    return axios.patch(`${orderSchoolProgramApiUrl}${programSlug}/`, {
      status: server.programOrderStatus.pendingAdminApproval,
      school: schoolSlug
    })
  },
}

export default program
