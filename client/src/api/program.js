import axios from 'axios'
import { getProgramsListApiUrl } from '../helpers/constants/constants'

const program = {
    getProgram(slug) {
        return axios.get(getProgramsListApiUrl + slug)
    },
    getProgramsList(params) {
        // :Object params: query params
        return axios.get(getProgramsListApiUrl, { params })
    },
}

export default program
