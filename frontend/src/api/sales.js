import request from './index'

export function saleBook(params) {
  return request.post('/sale/book', null, { params })
}

export function returnSale(params) {
  return request.put('/sale/return', null, { params })
}

export function searchSales(params) {
  return request.get('/sale/search/time', { params })
}

export function searchAllSales() {
  return request.get('/sale/search/all')
}
