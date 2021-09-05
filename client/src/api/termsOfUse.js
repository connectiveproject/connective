import axios from "axios"
import {
  UPDATE_TERMS_OF_USE_ACCEPTANCE_API_URL,
  GET_TERMS_OF_USE_TEXTS,
} from "@/helpers/constants/constants"

const termsOfUse = {
  updateTermsOfUseAcceptance() {
    // accept to tou agreement
    return axios.patch(UPDATE_TERMS_OF_USE_ACCEPTANCE_API_URL)
  },
  getTermsOfUseTexts() {
    return axios.get(GET_TERMS_OF_USE_TEXTS)
  },
}


export default termsOfUse
