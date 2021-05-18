import _ from "lodash"
import Vue from "vue"

function paginationToApiParams(pagination) {
  // convert & return pagination parameters to API parameters
  // :object pagination: pagination data parameters
  let apiParams = {}
  if (pagination.itemsPerPage) {
    apiParams._limit =
      pagination.itemsPerPage > 0 ? pagination.itemsPerPage : 99999
  }
  if (pagination.page) {
    apiParams._page = pagination.page
  }
  if (pagination.fieldFilters) {
    for (const [fieldName, value] of Object.entries(pagination.fieldFilters)) {
      let filters = value
      if (_.isArray(value)) {
        filters = value.map(filter => _.snakeCase(filter)).join()
      }
      apiParams[_.snakeCase(fieldName)] = filters
    }
  }
  if (pagination.searchFilter) {
    apiParams.q = pagination.searchFilter
  }
  if (pagination.sortBy && pagination.sortBy.length) {
    apiParams._sort = pagination.sortBy.map(item => _.snakeCase(item)).join()
  }
  if (pagination.sortDesc && pagination.sortDesc.length) {
    apiParams._order = pagination.sortDesc
      .map(isDesc => (isDesc ? "desc" : "asc"))
      .join()
  }
  return apiParams
}

function getDefaultState() {
  return {
    page: 1,
    itemsPerPage: 5,
    // { fieldName: 'string', fieldName: [array], ... }
    fieldFilters: {},
    // free-text search
    searchFilter: "",
    // ['field1', 'field2', ...]
    sortBy: [],
    // [true, false, ...]
    sortDesc: [],
  }
}

const pagination = {
  namespaced: true,
  state: getDefaultState(),
  mutations: {
    FLUSH_STATE(state) {
      Object.assign(state, getDefaultState())
    },
    UPDATE_PAGINATION(state, paginationParams) {
      // merge paginationParams to the state
      // Object paginationParams: contains keys of the keys to modify
      Object.assign(state, paginationParams)
    },
    INCREMENT_PAGE(state) {
      state.page += 1
    },
    ADD_FIELD_FILTER(state, { fieldName, value }) {
      // add filter to the group of field filters
      // :string fieldName: name of the field to filter
      // :Array/String value: the value to filter by
      Vue.set(state.fieldFilters, fieldName, value)
    },
    REMOVE_FIELD_FILTER(state, fieldName) {
      Vue.delete(state.fieldFilters, fieldName)
    },
  },
  getters: {
    apiParams: paginationToApiParams,
  },
  actions: {
    flushState({ commit }) {
      commit("FLUSH_STATE")
    },
    updatePagination({ commit }, paginationParams) {
      commit("UPDATE_PAGINATION", paginationParams)
    },
    incrementPage({ commit }) {
      commit("INCREMENT_PAGE")
    },
    addFieldFilter({ commit }, { fieldName, value }) {
      commit("ADD_FIELD_FILTER", { fieldName, value })
    },
    removeFieldFilter({ commit }, fieldName) {
      commit("REMOVE_FIELD_FILTER", fieldName)
    },
  },
}

export default pagination
