import axios from "axios"
import {
  GET_SCHOOL_DETAILS_API_URL,
  UPDATE_SCHOOL_DETAILS_API_URL,
  GET_SCHOOL_STUDENTS_LIST_API_URL,
  ADD_SCHOOL_STUDENTS_API_URL,
  DELETE_SCHOOL_STUDENTS_API_URL,
  EDIT_SCHOOL_STUDENTS_API_URL,
  GET_SCHOOL_COORDINATORS_LIST_API_URL,
  ADD_SCHOOL_COORDINATORS_API_URL,
  DELETE_SCHOOL_COORDINATORS_API_URL,
  EDIT_SCHOOL_COORDINATORS_API_URL,
} from "../helpers/constants/constants"

const school = {
  getSchoolDetails() {
    return axios.get(GET_SCHOOL_DETAILS_API_URL)
  },

  updateSchoolDetails(schoolSlug, data) {
    if (!schoolSlug)
      throw "updateSchoolDetails: received empty slug"
    return axios.put(`${UPDATE_SCHOOL_DETAILS_API_URL}${schoolSlug}/`, data)
  },

  getStudentList(params) {
    // :Object params: query params
    return axios.get(GET_SCHOOL_STUDENTS_LIST_API_URL, { params })
  },

  addStudent(student) {
    return axios.post(ADD_SCHOOL_STUDENTS_API_URL, student)
  },

  addStudents(csvFile) {
    // :File csvFile: file containing students to add to the school
    let formData = new FormData()
    formData.append("file", csvFile)
    return axios.post(ADD_SCHOOL_STUDENTS_API_URL, formData)
  },

  editStudent(slug, data) {
    if (!slug) throw "editStudent: received empty slug"
    return axios.patch(`${EDIT_SCHOOL_STUDENTS_API_URL}${slug}/`, data)
  },

  deleteStudents(studentSlugs) {
    return Promise.all(
      studentSlugs.map(slug =>
        axios.delete(`${DELETE_SCHOOL_STUDENTS_API_URL}${slug}`)
      )
    )
  },

  getCoordinatorList(params) {
    // :Object params: query params
    return axios.get(GET_SCHOOL_COORDINATORS_LIST_API_URL, { params })
  },

  addCoordinator(coordinator) {
    return axios.post(ADD_SCHOOL_COORDINATORS_API_URL, coordinator)
  },

  addCoordinators(csvFile) {
    // :File csvFile: file containing coordinators to add to the school
    let formData = new FormData()
    formData.append("file", csvFile)
    return axios.post(ADD_SCHOOL_COORDINATORS_API_URL, formData)
  },

  editCoordinator(slug, data) {
    if (!slug) throw "editCoordinator: received empty slug"
    return axios.patch(`${EDIT_SCHOOL_COORDINATORS_API_URL}${slug}/`, data)
  },

  deleteCoordinators(coordinatorSlugs) {
    return Promise.all(
      coordinatorSlugs.map(slug =>
        axios.delete(`${DELETE_SCHOOL_COORDINATORS_API_URL}${slug}`)
      )
    )
  },
}

export default school
