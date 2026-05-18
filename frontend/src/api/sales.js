import request from './index'

export function saleBook(params) {
  return request.post('/sale/book', null, { params })
}
