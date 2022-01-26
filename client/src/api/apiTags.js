import axios from "axios"
import {
  GET_ALL_TAGS_API_URL,
} from "../helpers/constants/constants"

const apiTags = {
  getAllTags() {
    return axios.get(GET_ALL_TAGS_API_URL)
  },
}

export default apiTags
