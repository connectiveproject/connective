import Api from "../../api"

function getDefaultState() {
  return {
    instructorList: [],
    totalInstructors: 0,
    vendorList: [],
    totalVendors: 0,
  }
}

const organization = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    ADD_INSTRUCTORS_TO_LIST(state, instructorList) {
      state.instructorList.push(...instructorList)
    },
    ADD_VENDORS_TO_LIST(state, vendorList) {
      state.vendorList.push(...vendorList)
    },
    SET_DETAILS(state, organizationDetails) {
      state.details = organizationDetails
    },
    SET_INSTRUCTOR_LIST(state, instructorList) {
      state.instructorList = instructorList
    },
    SET_INSTRUCTORS_TOTAL(state, total) {
      state.totalInstructors = total
    },
    SET_VENDOR_LIST(state, vendorList) {
      state.vendorList = vendorList
    },
    SET_VENDORS_TOTAL(state, total) {
      state.totalVendors = total
    },
  },
  getters: {
    organizationSlug(state) {
      return state.details.slug
    },
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    async getOrganizationDetails({ commit, state }) {
      if (!state.details.slug) {
        let res = await Api.organization.getOrganizationDetails()
        commit("SET_DETAILS", res.data)
      }
      return state.details
    },
    async getInstructorList(
      { commit, state, rootGetters },
      { override, usePagination }
    ) {
      // :boolean override: whether to override the list or not (i.e., extend)
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      const mutation = override
        ? "SET_INSTRUCTOR_LIST"
        : "ADD_INSTRUCTORS_TO_LIST"
      let res = await Api.organization.getInstructorList(params)
      commit(mutation, res.data.results)
      commit("SET_INSTRUCTORS_TOTAL", res.data.count)
      return state.instructorList
    },
    addInstructor(ctx, instructor) {
      return Api.organization.addInstructor(instructor)
    },
    addInstructors(ctx, csvFile) {
      return Api.organization.addInstructors(csvFile)
    },
    deleteInstructors(ctx, instructorSlugs) {
      return Api.organization.deleteInstructors(instructorSlugs)
    },
    editInstructor(ctx, { slug, instructor }) {
      return Api.organization.editInstructor(slug, instructor)
    },
    async getVendorList(
      { commit, state, rootGetters },
      { override, usePagination }
    ) {
      // :boolean override: whether to override the list or not (i.e., extend)
      const params = usePagination ? rootGetters["pagination/apiParams"] : {}
      const mutation = override ? "SET_VENDOR_LIST" : "ADD_VENDORS_TO_LIST"
      let res = await Api.organization.getVendorList(params)
      commit(mutation, res.data.results)
      commit("SET_VENDORS_TOTAL", res.data.count)
      return state.vendorList
    },
    addVendor(ctx, vendor) {
      return Api.organization.addVendor(vendor)
    },
    deleteVendors(ctx, vendorSlugs) {
      return Api.organization.deleteVendors(vendorSlugs)
    },
    editVendor(ctx, { slug, vendor }) {
      return Api.organization.editVendor(slug, vendor)
    },
  },
}

export default organization
