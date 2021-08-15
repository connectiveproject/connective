import axios from "axios"
import {
  GET_VENDOR_PROGRAM_GROUPS_API_URL,
  UPDATE_VENDOR_PROGRAM_GROUP_API_URL,
} from "../helpers/constants/constants"

const vendorProgramGroup = {
  getGroupList(params = {}) {
    return axios.get(GET_VENDOR_PROGRAM_GROUPS_API_URL, { params })
  },
  updateGroup(groupSlug, data) {
    if (!groupSlug) throw "updateGroup: received empty slug"
    return axios.patch(`${UPDATE_VENDOR_PROGRAM_GROUP_API_URL}${groupSlug}/`, data)
  },
}

export default vendorProgramGroup
