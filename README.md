# 图书销售管理系统

前后端分离的图书销售管理系统，面向书城管理员，覆盖进货、库存、销售、退货、财务统计全流程。

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3 + Element Plus + Axios + Pinia + Vue Router |
| 后端 | Python 3 + FastAPI + SQLAlchemy 2.0 (Async) |
| 数据库 | PostgreSQL |

## 目录结构

```
book_store/
├── main.py              # FastAPI 应用入口
├── database.py          # 数据库引擎与会话配置
├── models.py            # ORM 模型 (User/Book/Purchase/Sale/Bill)
├── schemas.py           # Pydantic 请求体校验
├── auth.py              # Token 管理、MD5 加密、认证依赖
├── routers/             # API 路由
│   ├── users.py         # 用户管理
│   ├── books.py         # 图书管理
│   ├── purchases.py     # 进货管理
│   ├── sales.py         # 销售管理
│   └── bills.py         # 财务管理
├── 建表.sql             # 数据库建表脚本
├── frontend/            # 前端项目
│   ├── src/
│   │   ├── api/         # Axios 请求封装
│   │   ├── router/      # 路由配置与守卫
│   │   ├── stores/      # Pinia 状态管理
│   │   ├── layout/      # 布局组件
│   │   └── views/       # 页面组件
│   ├── package.json
│   └── vite.config.js
└── 实验报告.md          # 详细实验报告
```

## 快速启动

### 1. 数据库

```bash
psql -U postgres -c "CREATE DATABASE bookstore_db"
psql -U postgres -d bookstore_db -f 建表.sql
```

### 2. 后端

```bash
pip install fastapi uvicorn sqlalchemy asyncpg pydantic
uvicorn main:app --reload --port 8000
```

API 文档：http://localhost:8000/docs

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

访问：http://localhost:3000

## 默认账户

数据库中需预置超级管理员：

```sql
-- 密码为 md5('admin123')
INSERT INTO users (username, user_password, user_role, real_name)
VALUES ('admin', '0192023a7bbd73250516f069df18b500', 'super_admin', '系统管理员');
```
