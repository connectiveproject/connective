import axios from "axios"
import {
  CREATE_FEED_POST_API_URL,
  CREATE_POST_IMAGES_API_URL,
} from "../helpers/constants/constants"

const eventFeedPost = {
  createFeedPost(data) {
    return axios.post(`${CREATE_FEED_POST_API_URL}`, data)
  },
  createPostImages(data) {
    return axios.post(`${CREATE_POST_IMAGES_API_URL}`, data)
  },
  getFeedPosts(params) {
    return axios.get(`${CREATE_FEED_POST_API_URL}`, { params })
  }
}

export default eventFeedPost
