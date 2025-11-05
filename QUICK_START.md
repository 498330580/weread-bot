# 🚀 WeRead Bot Web 版本 - 快速开始指南

## 📌 项目概述

WeRead Bot 已成功改造为 Flask Web 应用！现在可以通过现代化的Web界面来配置和管理微信读书自动阅读任务，无需接触命令行。

## ✨ 主要特性

- 🌐 **可视化Web界面** - 提供友好的用户界面
- ⚙️ **配置管理** - YAML编辑、导入导出配置文件
- 📊 **实时仪表板** - 监控任务状态、进度和日志
- 🎮 **任务控制** - 启动、停止、暂停阅读任务
- 📝 **日志查看** - 实时查看应用日志
- 🔌 **REST API** - 完整的API接口供第三方集成
- 📱 **响应式设计** - 支持桌面、平板和手机访问

## 📋 文件说明

| 文件 | 说明 |
|------|------|
| `app.py` | Flask 主应用程序 |
| `run.py` | 启动脚本（推荐使用） |
| `requirements.txt` | Python 依赖（已更新） |
| `services/` | 业务逻辑模块 |
| `templates/` | HTML 模板文件 |
| `config.yaml` | 配置文件 |
| `WEB_README.md` | 详细Web版文档 |

## 🎯 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 启动服务

**方式一：使用启动脚本（推荐）**
```bash
python run.py
```

**方式二：直接运行Flask**
```bash
python app.py
```

**方式三：Docker启动**
```bash
docker build -t weread-bot-web .
docker run -p 5000:5000 weread-bot-web
```

### 3️⃣ 访问Web界面

打开浏览器访问：
- 🏠 **主页/仪表板**: http://localhost:5000/
- ⚙️ **配置编辑**: http://localhost:5000/config
- 📊 **仪表板**: http://localhost:5000/dashboard

## 🎨 Web 界面功能

### 首页面板
- ✅ 应用状态监控
- 📈 任务进度显示
- ▶️ 快速操作按钮
- 📝 实时日志查看

### 配置页面
- 📝 YAML 编辑器
- 🔍 配置预览
- 💾 保存/导出/导入功能
- 🔧 分类配置面板

### 仪表板
- 📊 性能监控图表
- 📈 统计信息展示
- 📋 完整活动日志
- 🎮 任务控制按钮

## 🔧 配置方式

### 方式一：Web界面编辑（推荐）
1. 访问 http://localhost:5000/config
2. 在编辑区修改YAML配置
3. 点击"保存配置"按钮
4. 配置自动保存到 `config.yaml`

### 方式二：直接编辑文件
编辑项目根目录的 `config.yaml` 文件：

```yaml
app:
  name: WeReadBot
  startup_mode: immediate
  startup_delay: '60-300'

curl_config:
  file_path: curl_command.txt

reading:
  mode: smart_random
  target_duration: '60-70'
  reading_interval: '25-35'
  use_curl_data_first: true
```

### 方式三：环境变量
```bash
export FLASK_PORT=5000
export WEREAD_CURL_STRING="<你的curl命令>"
export TARGET_DURATION="60-70"
python run.py
```

## 🔌 REST API 接口

### 获取配置
```bash
curl http://localhost:5000/api/config
```

### 保存配置
```bash
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{...配置内容...}'
```

### 启动任务
```bash
curl -X POST http://localhost:5000/api/task/start
```

### 停止任务
```bash
curl -X POST http://localhost:5000/api/task/stop
```

### 获取日志
```bash
curl http://localhost:5000/api/logs?limit=100
```

### 导出配置
```bash
curl http://localhost:5000/api/export/config > config.yaml
```

### 导入配置
```bash
curl -X POST -F "file=@config.yaml" http://localhost:5000/api/import/config
```

### 健康检查
```bash
curl http://localhost:5000/api/health
```

## 📖 配置说明

所有配置项与原始版本相同，支持：

- **应用配置** - 名称、启动模式、启动延迟
- **CURL配置** - 文件路径或直接内容
- **阅读配置** - 模式、时长、间隔、智能随机参数
- **网络配置** - 超时、重试、频率限制
- **人类模拟** - 行为模拟、休息、User-Agent轮换
- **通知配置** - 多平台通知服务集成
- **定时配置** - Cron表达式、时区设置
- **守护进程** - 会话间隔、每日最大会话数
- **日志配置** - 级别、格式、文件位置

## 🔒 安全建议

1. **修改端口** - 避免使用默认5000端口
   ```bash
   FLASK_PORT=8080 python run.py
   ```

2. **启用HTTPS** - 使用反向代理（如nginx）添加SSL

3. **添加认证** - 可扩展添加简单的认证机制

4. **限制访问** - 使用防火墙限制访问IP

## 🐛 常见问题

### Q: 启动时出现"缺少必要的依赖"
**A:** 运行 `pip install -r requirements.txt` 安装依赖

### Q: 端口5000已被占用
**A:** 使用不同端口启动：
```bash
FLASK_PORT=8080 python run.py
```

### Q: Web界面加载缓慢
**A:** 
- 检查服务器资源
- 清除浏览器缓存
- 查看后台日志

### Q: 任务无法启动
**A:**
- 确保 `curl_command.txt` 存在且有效
- 检查 `logs/weread.log` 日志文件
- 验证微信读书账号未过期

### Q: 如何恢复为原始命令行版本？
**A:** 原始版本仍可用，运行：
```bash
python weread-bot.py --config config.yaml
```

## 🚀 部署到生产环境

### 使用 Gunicorn（推荐）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Docker Compose
创建 `docker-compose.yml`：
```yaml
version: '3.8'
services:
  weread-bot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_PORT=5000
      - WEREAD_CURL_STRING=<your-curl-command>
    volumes:
      - ./logs:/app/logs
      - ./config.yaml:/app/config.yaml
    restart: unless-stopped
```

启动：
```bash
docker-compose up -d
```

### 使用 Nginx 反向代理
```nginx
upstream weread_bot {
    server localhost:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://weread_bot;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📚 深入阅读

- 📖 [完整Web版文档](WEB_README.md)
- 📚 [原始项目README](README.md)
- 🔗 [项目GitHub地址](https://github.com/498330580/weread-bot)

## 💡 功能演进路线

已完成 ✅
- [x] Flask Web 框架
- [x] 可视化Web界面
- [x] 配置管理和编辑
- [x] REST API 接口
- [x] 日志管理
- [x] 任务控制

计划中 🚀
- [ ] 用户认证与权限管理
- [ ] 数据库持久化（SQLite/MySQL）
- [ ] WebSocket 实时日志推送
- [ ] 前端图表增强（Chart.js）
- [ ] 移动应用（React Native）
- [ ] 性能监控和告警
- [ ] 多语言支持

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**👏 感谢使用 WeRead Bot Web 版本！如有问题欢迎反馈。**

🌟 如果对你有帮助，请给个Star！
