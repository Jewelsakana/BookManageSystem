import request from './index'

export function login(data) {
  return request.post('/user/login', data)
}

export function logout() {
  return request.get('/user/logout')
}

export function register(data) {
  return request.post('/user/register', data)
}

export function updateUser(data) {
  return request.put('/user/update', data)
}

export function getUserView(params) {
  return request.get('/user/view', { params })
}
