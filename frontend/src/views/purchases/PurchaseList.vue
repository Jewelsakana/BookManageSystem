<template>
  <div>
    <h3>订单查询</h3>
    <el-button type="primary" @click="loadOrders" :loading="loading" style="margin-top: 16px">刷新列表</el-button>

    <el-table :data="orders" border style="width: 100%; margin-top: 16px" v-loading="loading">
      <el-table-column prop="order_id" label="订单号" width="80" />
      <el-table-column prop="book_id" label="图书编号" width="90" />
      <el-table-column prop="buy_price" label="进货价" width="100" />
      <el-table-column prop="purchase_quantity" label="数量" width="70" />
      <el-table-column prop="book_status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.book_status)">{{ statusLabel(row.book_status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_stocked" label="已入库" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_stocked === 'True' ? 'success' : 'info'">
            {{ row.is_stocked === 'True' ? '是' : '否' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="170" />
      <el-table-column prop="user_id" label="操作人ID" width="90" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { checkPurchases } from '../../api/purchases'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const orders = ref([])

const statusMap = { unpaid: '未付款', paid: '已付款', returned: '已退货' }
const typeMap = { unpaid: 'warning', paid: 'success', returned: 'info' }

function statusLabel(s) { return statusMap[s] || s }
function statusType(s) { return typeMap[s] || 'info' }

onMounted(() => {
  loadOrders()
})

async function loadOrders() {
  loading.value = true
  try {
    const res = await checkPurchases()
    orders.value = res.data
    ElMessage.success(`共 ${res.data.length} 条订单`)
  } catch (e) {
    orders.value = []
  } finally {
    loading.value = false
  }
}
</script>
