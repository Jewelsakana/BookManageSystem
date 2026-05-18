import request from './index'

export function searchBooks(params) {
  return request.get('/book/search', { params })
}

export function updateBook(data) {
  return request.put('/book/update', data)
}

export function addBook(params) {
  return request.put('/book/add', null, { params })
}
