import Api from "../../api"

function getDefaultState() {
  return {
    details: {
      slug: null,
      name: null,
      address: null,
      addressCity: null,
      zipCity: null,
      schoolCode: null,
      description: null,
      contactPhone: null,
      website: null,
      profilePicture: null,
      gradeLevels: [],
      lastUpdatedBy: null
    },
    studentList: [],
    totalStudents: 0,
    coordinatorList: [],
    totalCoordinators: 0,
  }
}

const school = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    ADD_STUDENTS_TO_LIST(state, studentList) {
      state.studentList.push(...studentList)
    },
    ADD_COORDINATORS_TO_LIST(state, coordinatorList) {
      state.coordinatorList.push(...coordinatorList)
    },
    SET_DETAILS(state, schoolDetails) {
      state.details = schoolDetails
    },
    SET_STUDENT_LIST(state, studentList) {
      state.studentList = studentList
    },
    SET_STUDENTS_TOTAL(state, total) {
      state.totalStudents = total
    },
    SET_COORDINATOR_LIST(state, coordinatorList) {
      state.coordinatorList = coordinatorList
    },
    SET_COORDINATORS_TOTAL(state, total) {
      state.totalCoordinators = total
    },
  },
  getters: {
    schoolSlug(state) {
      return state.details.slug
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getSchoolDetails({ commit, state }) {
      if (!state.details.slug) {
        let res = await Api.school.getSchoolDetails()
        commit("SET_DETAILS", res.data)
      }
      return state.details
    },
    async updateSchoolDetails({ commit, state }, { slug, schoolDetails }) {
      let res = await Api.school.updateSchoolDetails(slug, schoolDetails)
      commit("SET_DETAILS", res.data)
      return state.details
    },
    async getStudentList({ commit, state, rootGetters }, override = true) {
      // :boolean override: whether to override the list or not (i.e., extend)
      const params = rootGetters["pagination/apiParams"]
      const mutation = override ? "SET_STUDENT_LIST" : "ADD_STUDENTS_TO_LIST"
      let res = await Api.school.getStudentList(params)
      commit(mutation, res.data.results)
      commit("SET_STUDENTS_TOTAL", res.data.count)
      return state.studentList
    },
    addStudent(ctx, student) {
      return Api.school.addStudent(student)
    },
    addStudents(ctx, csvFile) {
      return Api.school.addStudents(csvFile)
    },
    deleteStudents(ctx, studentSlugs) {
      return Api.school.deleteStudents(studentSlugs)
    },
    editStudent(ctx, { slug, student }) {
      return Api.school.editStudent(slug, student)
    },
    async getCoordinatorList({ commit, state, rootGetters }, override = true) {
      // :boolean override: whether to override the list or not (i.e., extend)
      const params = rootGetters["pagination/apiParams"]
      const mutation = override ? "SET_COORDINATOR_LIST" : "ADD_COORDINATORS_TO_LIST"
      let res = await Api.school.getCoordinatorList(params)
      commit(mutation, res.data.results)
      commit("SET_COORDINATORS_TOTAL", res.data.count)
      return state.coordinatorList
    },
    addCoordinator(ctx, coordinator) {
      return Api.school.addCoordinator(coordinator)
    },
    addCoordinators(ctx, csvFile) {
      return Api.school.addCoordinators(csvFile)
    },
    deleteCoordinators(ctx, coordinatorSlugs) {
      return Api.school.deleteCoordinators(coordinatorSlugs)
    },
    editCoordinator(ctx, { slug, coordinator }) {
      return Api.school.editCoordinator(slug, coordinator)
    },
  },
}

export default school
