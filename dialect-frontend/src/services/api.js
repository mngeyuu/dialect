//import axios from 'axios'
//
//// 创建axios实例
//const api = axios.create({
//  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api/',
//  timeout: 10000,
//  headers: {
//    'Content-Type': 'application/json',
//    'Accept': 'application/json'
//  }
//})
//
//// 响应拦截器
//api.interceptors.response.use(
//  response => response,
//  error => {
//    console.error('API错误:', error.response || error)
//    return Promise.reject(error)
//  }
//)
//
//export default api
// src/services/api.js
import axios from 'axios'

// 开发时可用 devServer 代理，打包/Electron 时用环境变量或默认 localhost
const baseURL = process.env.VUE_APP_API_URL
  ? `${process.env.VUE_APP_API_URL.replace(/\/$/, '')}/api/`
  : 'http://localhost:8000/api/'

const api = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})
// 响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API错误:', error.response || error)
    return Promise.reject(error)
  }
)
export default api