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
    return axios.get(`${GET_PROGRAM_GROUPS_API_URL}${groupSlug}/`)
  },
  getGroupList(params) {
    return axios.get(GET_PROGRAM_GROUPS_API_URL, { params })
  },
  createGroup(payload) {
    return axios.post(CREATE_PROGRAM_GROUP_API_URL, payload)
  },
  updateGroup(groupSlug, payload) {
    return axios.patch(`${UPDATE_PROGRAM_GROUP_API_URL}${groupSlug}/`, payload)
  },
  deleteGroup(groupSlug) {
    return axios.delete(`${DELETE_PROGRAM_GROUP_API_URL}${groupSlug}/`)
  },
  getConsumers(groupSlug) {
    return axios.get(
      `${GET_PROGRAM_GROUP_CONSUMERS_API_URL}${groupSlug}/group_consumers/`
    )
  },
  updateGroupConsumers(groupSlug, consumerSlugs) {
    return axios.patch(
      `${UPDATE_PROGRAM_GROUP_CONSUMERS_API_URL}${groupSlug}/update_group_consumers/`,
      consumerSlugs
    )
  },
}

export default programGroup
