import request from './index'

export function checkBills(params) {
  return request.get('/bill/check', { params })
}

export function checkAllBills() {
  return request.get('/bill/checkall')
}
