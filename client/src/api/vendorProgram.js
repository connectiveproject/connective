import axios from "axios"
import {
  GET_VENDOR_PROGRAM_LIST_API_URL,
  GET_PROGRAM_MEDIA_LIST_API_URL,
  CREATE_PROGRAM_MEDIA_API_URL,
  DELETE_PROGRAM_MEDIA_API_URL,
  CREATE_VENDOR_PROGRAM_API_URL,
  UPDATE_VENDOR_PROGRAM_API_URL,
  DELETE_VENDOR_PROGRAM_API_URL,
} from "../helpers/constants/constants"

const vendorProgram = {
  getProgram(slug) {
    return axios.get(`${GET_VENDOR_PROGRAM_LIST_API_URL}${slug}/`)
  },
  getProgramMediaList(programSlug) {
    if (!programSlug)
      throw "getProgramMediaList: received empty slug"
    return axios.get(GET_PROGRAM_MEDIA_LIST_API_URL, {
      params: {
        activity__slug: programSlug,
      },
    })
  },
  deleteProgramMedia(mediaSlug) {
    if (!mediaSlug)
      throw "deleteProgramMedia: received empty slug"
    return axios.delete(`${DELETE_PROGRAM_MEDIA_API_URL}${mediaSlug}/`)
  },
  createProgramMedia(data) {
    return axios.post(CREATE_PROGRAM_MEDIA_API_URL, data)
  },
  getProgramList(params = null) {
    // :Object params: query params
    if (params) {
      return axios.get(GET_VENDOR_PROGRAM_LIST_API_URL, { params })
    }
    return axios.get(GET_VENDOR_PROGRAM_LIST_API_URL)
  },
  createProgram(data) {
    return axios.post(CREATE_VENDOR_PROGRAM_API_URL, data)
  },
  updateProgram(programSlug, data) {
    if (!programSlug) throw "updateProgram: received empty slug"
    return axios.patch(`${UPDATE_VENDOR_PROGRAM_API_URL}${programSlug}/`, data)
  },
  deleteProgram(programSlug) {
    if (!programSlug) throw "deleteProgram: received empty slug"
    return axios.delete(`${DELETE_VENDOR_PROGRAM_API_URL}${programSlug}/`)
  },
}

export default vendorProgram
