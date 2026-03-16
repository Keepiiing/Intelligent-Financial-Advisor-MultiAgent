# 智能金融顾问系统（Multi-Agent 方向）

一个可直接运行的、面向 GitHub 展示和二次扩展的金融顾问项目骨架。项目采用企业常见的分层方式实现了一个可演示的 Multi-Agent MVP：主 Agent 负责理解需求和编排流程，风险评估 Agent、投资推荐 Agent、合规检查 Agent、内容过滤 Agent 负责执行具体任务，最终通过 FastAPI 提供服务接口。

这个仓库的目标不是一次性还原完整金融生产系统，而是提供一个“能部署、能演示、结构清晰、便于维护和扩展”的基础版本。默认使用本地示例数据运行，无需外部依赖即可完成端到端演示；当你需要接入真实的市场数据 API、Milvus、Neo4j、vLLM 时，可以直接替换 `app/services` 与 `app/repositories` 下的适配层实现。

## 1. 核心能力

- 支持自然语言投资需求输入。
- 支持主 Agent 拆解任务并串联多 Agent 流程。
- 支持风险评估、组合推荐、合规校验、敏感信息过滤。
- 支持本地示例产品库和模拟市场数据。
- 支持 Docker 启动与本地快速启动。
- 提供健康检查、投资建议接口和基础测试。

## 2. 技术栈

- Python 3.11
- FastAPI
- LangGraph（默认优先使用，未安装时自动降级为本地编排）
- Pydantic / pydantic-settings
- Uvicorn
- Pytest
- Docker / Docker Compose

## 3. 项目结构

```text
智能金融顾问系统-MultiAgent
├── app
│   ├── agents
│   ├── api
│   ├── core
│   ├── domain
│   ├── orchestrator
│   ├── repositories
│   ├── schemas
│   ├── services
│   └── main.py
├── data
│   └── products.json
├── tests
│   └── test_advisor_flow.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.markdown
├── 需求文档.md
└── 工作流程文档.md
```

## 4. 运行方式

### 4.1 本地启动

1. 创建虚拟环境并安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 复制环境变量模板：

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

3. 启动服务：

```bash
uvicorn app.main:app --reload
```

4. 打开接口文档：

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4.2 Docker 启动

```bash
docker compose up --build
```

启动后访问：

- API: [http://localhost:8000](http://localhost:8000)
- 文档: [http://localhost:8000/docs](http://localhost:8000/docs)

## 5. 快速体验

### 5.1 健康检查

```bash
curl http://localhost:8000/health
```

### 5.2 生成投资建议

```bash
curl -X POST http://localhost:8000/api/v1/advice \
  -H "Content-Type: application/json" \
  -d '{
    "query": "我有50万本金，风险中等，想配置海外基金，投资周期24个月",
    "profile": {
      "user_id": "demo-user",
      "name": "张三",
      "investable_amount_cny": 500000,
      "risk_preference": "balanced",
      "investment_horizon_months": 24,
      "current_assets_cny": 1200000,
      "monthly_cash_need_cny": 15000,
      "annual_fx_quota_usd": 50000,
      "used_fx_quota_usd": 10000
    }
  }'
```

## 6. 核心架构说明

### 6.1 Agent 分工

- 主 Agent：提取用户意图、识别缺失参数、决定流程走向。
- 风险评估 Agent：根据用户画像计算风险等级和适配资产类型。
- 投资推荐 Agent：从产品库中筛选产品并生成保守/均衡/进取三套方案。
- 合规检查 Agent：检查外汇额度、风险匹配、产品适格性。
- 内容过滤 Agent：过滤敏感字段并生成面向用户的结构化输出。

### 6.2 分层原则

- `api` 层只负责输入输出和依赖注入。
- `agents` 层只负责单职责业务执行。
- `services` 层负责可替换的规则、检索、市场数据、脱敏逻辑。
- `repositories` 层负责读取底层数据源。
- `orchestrator` 层负责把多个 Agent 串成完整流程。

这种结构适合后续替换真实依赖，例如：

- 把 `ProductRepository` 换成 Milvus + Neo4j 检索。
- 把 `MarketDataService` 换成真实市场数据 API。
- 把 `AdvisorWorkflow` 接入真实 LangGraph + vLLM 推理链路。

## 7. 配置说明

环境变量示例见 `.env.example`：

- `APP_NAME`：应用名称。
- `ENVIRONMENT`：运行环境。
- `API_PREFIX`：接口前缀。
- `USE_SAMPLE_DATA`：是否使用本地示例数据。
- `DEFAULT_FX_LIMIT_USD`：默认年度购汇额度。
- `USD_CNY_RATE`：汇率换算参数。

## 8. 测试

执行测试：

```bash
pytest
```

## 9. 二次扩展建议

- 接入真实 LLM：在 `agents` 层接入 Prompt 模板和模型客户端。
- 接入向量库：在 `repositories` 层替换为 Milvus 检索实现。
- 接入知识图谱：为合规与产品关系推理增加 Neo4j 查询。
- 增加登录鉴权：在 `api` 层增加 JWT 或网关鉴权。
- 增加数据库：落地审计日志、会话记录、用户画像更新记录。
- 增加任务队列：对定时同步、推荐重算、监控告警做异步化处理。

## 10. 项目文档

- [需求文档.md](./需求文档.md)
- [工作流程文档.md](./工作流程文档.md)
