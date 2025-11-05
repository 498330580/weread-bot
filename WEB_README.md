# WeRead Bot Web 版本使用指南

## 🎉 欢迎使用 WeRead Bot Web 版本

这是一个基于 Flask 的Web版本微信读书阅读机器人，提供可视化的Web界面来配置和管理阅读任务。

## 📋 目录结构

```
weread-bot/
├── app.py                      # Flask 应用主程序
├── run.py                      # 启动脚本
├── config.yaml                 # 配置文件
├── requirements.txt            # Python 依赖
├── templates/                  # HTML 模板
│   ├── index.html             # 首页与仪表板
│   ├── config.html            # 配置编辑页面
│   └── dashboard.html         # 仪表板页面
├── static/                    # 静态资源（CSS、JS）
├── services/                  # 业务逻辑模块
│   ├── __init__.py
│   ├── config_manager.py      # 配置管理器
│   ├── task_manager.py        # 任务管理器
│   └── log_manager.py         # 日志管理器
└── logs/                      # 日志文件目录
    └── weread.log             # 应用日志
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python run.py
```

或直接运行Flask应用：

```bash
python app.py
```

### 3. 访问Web界面

打开浏览器访问：http://localhost:5000

## 🌐 Web界面功能

### 首页 (/)
- 📊 应用状态与任务监控
- ⏱️ 实时进度条
- 📝 日志查看
- 🎮 快速操作按钮

### 仪表板 (/dashboard)
- 📈 性能监控
- 📊 统计信息
- 📋 活动日志
- 🎮 任务控制

### 配置 (/config)
- ⚙️ 可视化配置编辑
- 📄 YAML编辑器
- 💾 保存/导出/导入
- 🔄 重置为默认配置

## 🔌 REST API 接口

### 配置管理

**获取配置**
```
GET /api/config
```

**保存配置**
```
POST /api/config
Content-Type: application/json

{...配置内容...}
```

**导出配置**
```
GET /api/export/config
```

**导入配置**
```
POST /api/import/config
Content-Type: multipart/form-data

file: <配置文件>
```

### 任务控制

**启动任务**
```
POST /api/task/start
```

**停止任务**
```
POST /api/task/stop
```

**获取任务状态**
```
GET /api/task/status
```

### 日志管理

**获取日志**
```
GET /api/logs?limit=100
```

**清空日志**
```
POST /api/logs/clear
```

**下载日志**
```
GET /api/logs/download
```

### 健康检查

**健康检查**
```
GET /api/health
```

## ⚙️ 环境变量配置

在系统环境变量或 `.env` 文件中设置：

```env
# Flask 配置
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# WeRead Bot 配置
WEREAD_CURL_STRING=<你的CURL命令>
# 或
WEREAD_CURL_BASH_FILE_PATH=curl_command.txt

# 其他配置
TARGET_DURATION=60-70
READING_MODE=smart_random
```

## 📝 配置文件格式

配置文件采用 YAML 格式，示例：

```yaml
app:
  name: WeReadBot
  version: '0.3.1'
  startup_mode: immediate
  startup_delay: '60-300'

curl_config:
  file_path: curl_command.txt

reading:
  mode: smart_random
  target_duration: '60-70'
  reading_interval: '25-35'
  use_curl_data_first: true
  fallback_to_config: true
  books: []
  smart_random:
    book_continuity: 0.8
    chapter_continuity: 0.7
    book_switch_cooldown: 300

human_simulation:
  enabled: true
  reading_speed_variation: true
  break_probability: 0.15
  break_duration: '30-180'
  rotate_user_agent: false

network:
  timeout: 30
  retry_times: 3
  retry_delay: '5-15'
  rate_limit: 10

notification:
  enabled: true
  include_statistics: true
  channels: []

schedule:
  enabled: false
  cron_expression: '0 */2 * * *'
  timezone: Asia/Shanghai

daemon:
  enabled: false
  session_interval: '120-180'
  max_daily_sessions: 12

logging:
  level: INFO
  format: detailed
  file: logs/weread.log
  max_size: '10MB'
  backup_count: 5
  console: true
```

## 🔧 Docker 运行

### 构建镜像

```bash
docker build -t weread-bot-web .
```

### 运行容器

```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_PORT=5000 \
  -e WEREAD_CURL_STRING="<你的CURL命令>" \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config.yaml:/app/config.yaml \
  --name weread-bot-web \
  weread-bot-web
```

## 🔒 安全建议

1. **修改默认端口**：建议在生产环境中改用高端口
2. **启用认证**：可以添加简单的身份认证机制
3. **使用HTTPS**：建议在反向代理中使用HTTPS
4. **限制访问**：使用防火墙限制Web服务访问IP

## 🐛 故障排查

### 端口已占用

如果 5000 端口已被占用，可以修改：

```bash
FLASK_PORT=8080 python run.py
```

### CURL 命令获取失败

1. 检查 `curl_command.txt` 文件是否存在
2. 确保CURL命令格式正确
3. 检查环境变量 `WEREAD_CURL_STRING` 是否正确设置

### 任务无法启动

1. 查看日志文件 `logs/weread.log`
2. 确保微信读书账号未过期
3. 检查网络连接是否正常

### Web 界面加载缓慢

1. 检查服务器资源（CPU/内存）
2. 尝试清空浏览器缓存
3. 检查网络连接

## 📚 原始功能说明

Web 版本完全兼容原始的命令行版本，支持所有原有功能：

- ✅ 多用户支持
- ✅ 多种运行模式（立即执行、定时、守护进程）
- ✅ 智能阅读模式
- ✅ 人类行为模拟
- ✅ 多平台通知
- ✅ 详细统计报告

## 📖 更多信息

- 📝 原项目文档：[README.md](README.md)
- 🔗 项目地址：https://github.com/498330580/weread-bot
- 💬 问题反馈：请提交 Issue

## 📄 许可证

MIT License

## 贡献者

感谢所有为这个项目做出贡献的人！

---

**祝你使用愉快！如有问题欢迎反馈。** 🎉
