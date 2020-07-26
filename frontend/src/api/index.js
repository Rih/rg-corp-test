import axios from 'axios'
import {
  URL_BASE
} from '../globals';

const defaultConfig = {
  baseURL: URL_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json: charset=utf-8'
  },
}

export default axios.create(
   defaultConfig
)
