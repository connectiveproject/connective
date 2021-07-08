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
    return axios.get(GET_PROGRAM_MEDIA_LIST_API_URL, {
      params: {
        activity__slug: programSlug,
      },
    })
  },
  deleteProgramMedia(mediaSlug) {
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
    return axios.patch(
      `${UPDATE_VENDOR_PROGRAM_API_URL}${programSlug}/`,
      data
    )
  },
  deleteProgram(programSlug) {
    return axios.delete(`${DELETE_VENDOR_PROGRAM_API_URL}${programSlug}/`)
  },
}

export default vendorProgram
