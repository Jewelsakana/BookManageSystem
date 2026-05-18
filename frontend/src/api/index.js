import axios from 'axios'
import { ElMessage } from 'element-plus'

//axios实例
const request = axios.create({
  baseURL: '',
  timeout: 10000
})

//请求拦截器，每次请求自动从localStorage取出token放入Authorization头
request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = token
  }
  return config
})

//响应拦截器：统一弹出错误提示，401时清空登录态，跳转到登录页
request.interceptors.response.use(
  response => response,
  error => {
    const msg = error.response?.data?.detail || '请求失败'
    ElMessage.error(msg)
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default request
