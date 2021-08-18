import axios from "axios"
import {
  GET_PROGRAM_GROUPS_API_URL,
  CREATE_PROGRAM_GROUP_API_URL,
  GET_PROGRAM_GROUP_CONSUMERS_API_URL,
  UPDATE_PROGRAM_GROUP_CONSUMERS_API_URL,
  UPDATE_PROGRAM_GROUP_API_URL,
  DELETE_PROGRAM_GROUP_API_URL,
} from "../helpers/constants/constants"

const programGroup = {
  getGroup(groupSlug) {
    if (!groupSlug) throw "getGroup: received empty slug"
    return axios.get(`${GET_PROGRAM_GROUPS_API_URL}${groupSlug}/`)
  },
  getGroupList(params = {}) {
    return axios.get(GET_PROGRAM_GROUPS_API_URL, { params })
  },
  createGroup(data) {
    return axios.post(CREATE_PROGRAM_GROUP_API_URL, data)
  },
  updateGroup(groupSlug, data) {
    if (!groupSlug) throw "updateGroup: received empty slug"
    return axios.patch(`${UPDATE_PROGRAM_GROUP_API_URL}${groupSlug}/`, data)
  },
  deleteGroup(groupSlug) {
    if (!groupSlug) throw "deleteGroup: received empty slug"
    return axios.delete(`${DELETE_PROGRAM_GROUP_API_URL}${groupSlug}/`)
  },
  getConsumers(groupSlugs, params) {
    if (!groupSlugs) throw "getConsumers: received empty slug"
    return axios.get(GET_PROGRAM_GROUP_CONSUMERS_API_URL, {
      params: { ...params, slugs: groupSlugs.join(",") },
    })
  },
  updateGroupConsumers(groupSlug, consumerSlugs) {
    if (!groupSlug) {
      throw "updateGroupConsumers: received empty slug"
    }
    return axios.patch(
      `${UPDATE_PROGRAM_GROUP_CONSUMERS_API_URL}${groupSlug}/update_group_consumers/`,
      consumerSlugs
    )
  },
}

export default programGroup
