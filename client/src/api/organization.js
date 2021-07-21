import axios from "axios"
import {
  GET_ORGANIZATION_INSTRUCTORS_LIST_API_URL,
  ADD_ORGANIZATION_INSTRUCTORS_API_URL,
  DELETE_ORGANIZATION_INSTRUCTORS_API_URL,
  EDIT_ORGANIZATION_INSTRUCTORS_API_URL,
  GET_ORGANIZATION_VENDORS_LIST_API_URL,
  ADD_ORGANIZATION_VENDORS_API_URL,
  DELETE_ORGANIZATION_VENDORS_API_URL,
  EDIT_ORGANIZATION_VENDORS_API_URL,
} from "../helpers/constants/constants"

const organization = {
  getInstructorList(params) {
    // :Object params: query params
    return axios.get(GET_ORGANIZATION_INSTRUCTORS_LIST_API_URL, { params })
  },

  addInstructor(instructor) {
    return axios.post(ADD_ORGANIZATION_INSTRUCTORS_API_URL, instructor)
  },

  editInstructor(slug, data) {
    if (!slug) throw "editInstructor: received empty slug"
    return axios.patch(`${EDIT_ORGANIZATION_INSTRUCTORS_API_URL}${slug}/`, data)
  },

  deleteInstructors(instructorSlugs) {
    return Promise.all(
      instructorSlugs.map(slug =>
        axios.delete(`${DELETE_ORGANIZATION_INSTRUCTORS_API_URL}${slug}/`)
      )
    )
  },

  getVendorList(params) {
    // :Object params: query params
    return axios.get(GET_ORGANIZATION_VENDORS_LIST_API_URL, { params })
  },

  addVendor(vendor) {
    return axios.post(ADD_ORGANIZATION_VENDORS_API_URL, vendor)
  },

  editVendor(slug, data) {
    if (!slug) throw "editVendor: received empty slug"
    return axios.patch(`${EDIT_ORGANIZATION_VENDORS_API_URL}${slug}/`, data)
  },

  deleteVendors(vendorSlugs) {
    return Promise.all(
      vendorSlugs.map(slug =>
        axios.delete(`${DELETE_ORGANIZATION_VENDORS_API_URL}${slug}/`)
      )
    )
  },
}

export default organization
