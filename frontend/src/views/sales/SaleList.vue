<template>
  <div>
    <h3>销售记录查询</h3>
    <el-form inline style="margin-top: 16px">
      <el-form-item label="开始时间">
        <el-date-picker v-model="first_time" type="datetime" placeholder="选择开始时间" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DDTHH:mm:ss" />
      </el-form-item>
      <el-form-item label="结束时间">
        <el-date-picker v-model="last_time" type="datetime" placeholder="选择结束时间" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DDTHH:mm:ss" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch" :loading="loading">查询</el-button>
        <el-button v-if="userStore.isSuperAdmin" type="warning" @click="handleSearchAll" :loading="loadingAll">查看全部</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="sales" border style="width: 100%; margin-top: 12px" v-loading="loading || loadingAll">
      <el-table-column prop="sale_id" label="销售号" width="80" />
      <el-table-column prop="isbn" label="ISBN" width="150" />
      <el-table-column prop="title" label="书名" min-width="180" />
      <el-table-column prop="sale_price" label="售价" width="90" />
      <el-table-column prop="sale_quantity" label="数量" width="70" />
      <el-table-column prop="sale_status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.sale_status === 'completed' ? 'success' : 'info'">
            {{ row.sale_status === 'completed' ? '已完成' : '已退货' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="sold_at" label="销售时间" width="170" />
      <el-table-column v-if="userStore.isSuperAdmin" prop="user_id" label="操作人ID" width="90" />
      <el-table-column label="操作" width="80" fixed="right">
        <template #default="{ row }">
          <el-button type="danger" size="small" :disabled="row.sale_status !== 'completed'" @click="handleReturn(row)">
            退货
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { searchSales, searchAllSales, returnSale } from '../../api/sales'
import { useUserStore } from '../../stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const loading = ref(false)
const loadingAll = ref(false)
const first_time = ref('')
const last_time = ref('')
const sales = ref([])

async function handleSearch() {
  if (!first_time.value || !last_time.value) {
    ElMessage.warning('请选择开始和结束时间')
    return
  }
  loading.value = true
  try {
    const res = await searchSales({ first_time: first_time.value, last_time: last_time.value })
    sales.value = res.data
    if (res.data.length === 0) {
      ElMessage.info('该时间段内无销售记录')
    } else {
      ElMessage.success(`共 ${res.data.length} 条销售记录`)
    }
  } catch (e) {
    sales.value = []
  } finally {
    loading.value = false
  }
}

async function handleReturn(row) {
  try {
    await ElMessageBox.confirm(`确认对销售号 ${row.sale_id}（${row.title}）进行退货？库存将自动回增。`, '确认退货', { type: 'warning' })
  } catch (e) {
    return
  }
  try {
    await returnSale({ sale_id: row.sale_id })
    ElMessage.success('退货成功')
    sales.value = []  // clear, let user re-query
  } catch (e) {
    // handled by interceptor
  }
}

async function handleSearchAll() {
  loadingAll.value = true
  try {
    const res = await searchAllSales()
    sales.value = res.data
    if (res.data.length === 0) {
      ElMessage.info('无销售记录')
    } else {
      ElMessage.success(`共 ${res.data.length} 条销售记录`)
    }
  } catch (e) {
    sales.value = []
  } finally {
    loadingAll.value = false
  }
}
</script>
