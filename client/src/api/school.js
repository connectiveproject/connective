import axios from "axios"
import {
  GET_SCHOOL_DETAILS_API_URL,
  UPDATE_SCHOOL_DETAILS_API_URL,
  GET_SCHOOL_STUDENTS_LIST_API_URL,
  ADD_SCHOOL_STUDENTS_API_URL,
  DELETE_SCHOOL_STUDENTS_API_URL,
  EDIT_SCHOOL_STUDENTS_API_URL,
} from "../helpers/constants/constants"

const school = {
  getSchoolDetails() {
    return axios.get(GET_SCHOOL_DETAILS_API_URL)
  },

  updateSchoolDetails(schoolSlug, payload) {
    return axios.put(`${UPDATE_SCHOOL_DETAILS_API_URL}${schoolSlug}/`, payload)
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

  editStudent(slug, payload) {
    return axios.patch(`${EDIT_SCHOOL_STUDENTS_API_URL}${slug}/`, payload)
  },

  deleteStudents(studentSlugs) {
    return Promise.all(
      studentSlugs.map(slug =>
        axios.delete(`${DELETE_SCHOOL_STUDENTS_API_URL}${slug}`)
      )
    )
  },
}

export default school
