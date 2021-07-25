import isArray from "lodash/isArray"
import Utils from "../../helpers/utils"

import Vue from "vue"

function paginationToApiParams(pagination) {
  // convert & return pagination parameters to API parameters
  // :object pagination: pagination data parameters
  let apiParams = {}
  if (pagination.itemsPerPage) {
    apiParams.page_size =
      pagination.itemsPerPage > 0 ? pagination.itemsPerPage : 99999
  }
  if (pagination.page) {
    apiParams.page = pagination.page
  }
  if (pagination.fieldFilters) {
    for (const [fieldName, value] of Object.entries(pagination.fieldFilters)) {
      let filters = value
      if (isArray(value)) {
        filters = value.map(filter => Utils.camelToSnakeCase(filter)).join()
      }
      apiParams[Utils.camelToSnakeCase(fieldName)] = filters
    }
  }
  if (pagination.searchFilter) {
    apiParams.search = pagination.searchFilter
  }
  if (pagination.sortBy && pagination.sortBy.length) {
    const order = []
    for (let i = 0; i < pagination.sortBy.length; i++) {
      if (pagination.sortDesc[i] !== false) {
        // if undefined or True:
        order.push(Utils.camelToSnakeCase(pagination.sortBy[i]))
      } else {
        order.push(`-${Utils.camelToSnakeCase(pagination.sortBy[i])}`)
      }
    }
    apiParams.ordering = order.join()
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
    tagFilters: [],
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
