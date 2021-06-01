import axios from "axios"
import {
  getSchoolDetailsApiUrl,
  updateSchoolDetailsApiUrl,
  getSchoolStudentListApiUrl,
  addSchoolStudentsApiUrl,
  deleteSchoolStudentsApiUrl,
  editSchoolStudentsApiUrl,
} from "../helpers/constants/constants"

const school = {
  getSchoolDetails() {
    return axios.get(getSchoolDetailsApiUrl)
  },

  updateSchoolDetails(schoolSlug, payload) {
    return axios.put(`${updateSchoolDetailsApiUrl}${schoolSlug}/`, payload)
  },

  getStudentList(params) {
    // :Object params: query params
    return axios.get(getSchoolStudentListApiUrl, { params })
  },

  addStudent(student) {
    return axios.post(addSchoolStudentsApiUrl, student)
  },

  addStudents(csvFile) {
    // :File csvFile: file containing students to add to the school
    let formData = new FormData()
    formData.append("file", csvFile)
    return axios.post(addSchoolStudentsApiUrl, formData)
  },

  editStudent(slug, payload) {
    return axios.patch(`${editSchoolStudentsApiUrl}${slug}/`, payload)
  },

  deleteStudents(studentSlugs) {
    return Promise.all(
      studentSlugs.map(slug =>
        axios.delete(`${deleteSchoolStudentsApiUrl}${slug}`)
      )
    )
  },
}

export default school
