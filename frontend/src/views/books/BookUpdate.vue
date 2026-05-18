<template>
  <div>
    <h3>图书信息修改</h3>
    <el-form :model="form" label-width="100px" style="max-width: 500px; margin-top: 16px">
      <el-form-item label="书籍编号">
        <el-input-number v-model="form.book_id" :min="1" placeholder="输入书籍编号" style="width: 100%" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadBook" :loading="loadingBook">加载图书信息</el-button>
      </el-form-item>

      <el-divider />

      <el-form-item label="书名">
        <el-input v-model="form.title" placeholder="书名" clearable />
      </el-form-item>
      <el-form-item label="作者">
        <el-input v-model="form.author" placeholder="作者" clearable />
      </el-form-item>
      <el-form-item label="出版社">
        <el-input v-model="form.publisher" placeholder="出版社" clearable />
      </el-form-item>
      <el-form-item label="零售价">
        <el-input-number v-model="form.price" :min="0" :precision="2" style="width: 100%" />
      </el-form-item>
      <el-form-item>
        <el-button type="success" @click="handleUpdate" :loading="loading">提交修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { searchBooks, updateBook } from '../../api/books'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const loadingBook = ref(false)

const form = reactive({
  book_id: null,
  title: '',
  author: '',
  publisher: '',
  price: null
})

async function loadBook() {
  if (!form.book_id) {
    ElMessage.warning('请输入书籍编号')
    return
  }
  loadingBook.value = true
  try {
    const res = await searchBooks({ book_id: form.book_id })
    const book = res.data[0]
    if (book) {
      form.title = book.title || ''
      form.author = book.author || ''
      form.publisher = book.publisher || ''
      form.price = book.price
      ElMessage.success('图书信息加载成功')
    } else {
      ElMessage.error('未找到该书籍')
    }
  } catch (e) {
    // handled by interceptor
  } finally {
    loadingBook.value = false
  }
}

async function handleUpdate() {
  if (!form.book_id) {
    ElMessage.warning('请输入书籍编号')
    return
  }
  loading.value = true
  try {
    const data = { book_id: form.book_id }
    if (form.title) data.title = form.title
    if (form.author) data.author = form.author
    if (form.publisher) data.publisher = form.publisher
    if (form.price !== null && form.price !== undefined) data.price = form.price
    await updateBook(data)
    ElMessage.success('书籍更新成功')
  } catch (e) {
    // handled by interceptor
  } finally {
    loading.value = false
  }
}
</script>
