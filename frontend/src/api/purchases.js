import request from './index'

export function addPurchase(data) {
  return request.post('/purchase/add', data)
}

export function payPurchase(params) {
  return request.post('/purchase/pay', null, { params })
}

export function returnPurchase(params) {
  return request.put('/purchase/return', null, { params })
}

export function checkPurchases() {
  return request.get('/purchase/check')
}
