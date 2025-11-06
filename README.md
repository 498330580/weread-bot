# WeRead Bot: 微信读书自动阅读机器人

[![Docker Automated build](https://img.shields.io/docker/automated/498330580/weread-bot?style=flat-square)](https://hub.docker.com/r/498330580/weread-bot/)
[![Docker Tags](https://img.shields.io/docker/v/498330580/weread-bot?sort=semver&style=flat-square&label=docker%20image)](https://hub.docker.com/r/498330580/weread-bot/)
[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/498330580/weread-bot?style=flat-square)](https://hub.docker.com/r/498330580/weread-bot/)
[![Release](https://img.shields.io/github/release/498330580/weread-bot?style=flat-square)](https://github.com/498330580/weread-bot/releases)
[![Docker Build](https://img.shields.io/github/actions/workflow/status/498330580/weread-bot/docker-build.yml?style=flat-square&label=Docker%20Build)](https://github.com/498330580/weread-bot/actions/workflows/docker-build.yml)
[![Release Build](https://img.shields.io/github/actions/workflow/status/498330580/weread-bot/release.yml?style=flat-square&label=Release)](https://github.com/498330580/weread-bot/actions/workflows/release.yml)
[![Pages Deploy](https://img.shields.io/github/actions/workflow/status/498330580/weread-bot/page.yml?style=flat-square&label=Pages)](https://github.com/498330580/weread-bot/actions/workflows/page.yml)
[![Commit activity](https://img.shields.io/github/commit-activity/m/498330580/weread-bot?style=flat-square)](https://hub.docker.com/r/498330580/weread-bot/)
[![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/498330580/weread-bot?style=flat-square)](https://github.com/498330580/weread-bot/blob/main/LICENSE)

WeRead Bot 是一个功能完善的微信读书自动阅读机器人，现已改造为现代化的 Flask Web 应用！通过模拟真实用户阅读行为来积累阅读时长，支持多用户、多种运行模式、可视化Web界面配置。

## 📋 目录

- [核心特性](#核心特性)
- [运行预览](#运行预览)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [运行模式](#运行模式)
- [部署方式](#部署方式)
- [常见问题](#常见问题)
- [技术支持](#技术支持)

## 核心特性

### 🌐 现代化Web界面
- **可视化配置编辑** - YAML编辑器和分类配置面板
- **实时任务监控** - 仪表板显示性能、统计信息、活动日志
- **完整REST API** - 第三方系统集成
- **响应式设计** - 支持桌面、平板和手机访问

### ⚙️ 核心功能
- **智能延迟** - 启动随机延迟，防止固定特征识别
- **灵活阅读** - 支持时长区间配置（如 30-90 分钟随机）
- **多用户支持** - 多个账号顺序执行，独立配置
- **多种阅读模式** - 智能随机、顺序阅读、纯随机
- **高级行为模拟** - 阅读速度变化、中途休息、User-Agent轮换
- **详细统计报告** - 完整的阅读数据和多维度分析

### 🔧 配置灵活性
- **多样化配置** - 配置文件、环境变量、Web界面三种方式
- **智能配置解析** - 从CURL命令自动提取数据
- **精准请求模拟** - 动态生成签名和校验

### 📱 通知和任务
- **多平台通知** - 支持12种通知服务（PushPlus、Telegram、钉钉等）
- **灵活定时任务** - Cron表达式定时执行
- **守护进程模式** - 长期运行，自动管理会话
- **GitHub Actions** - 云端自动化支持

### 🐳 部署友好
- **Docker支持** - 提供Dockerfile和docker-compose配置
- **一键启动** - `python run.py` 即可启动Web服务
- **环境隔离** - 虚拟环境配置简单

## 运行预览

```
🚀 Flask服务启动中...

📝 配置信息:
   • 地址: http://0.0.0.0:5000
   • 调试模式: 关闭
   • 日志: logs/weread.log
   • 配置文件: config.yaml

🌐 访问地址:
   • 主页: http://localhost:5000/
   • 仪表板: http://localhost:5000/dashboard
   • 配置: http://localhost:5000/config
   • API: http://localhost:5000/api/health
```

## 界面展示

### 配置编辑页面
![配置编辑](https://raw.githubusercontent.com/498330580/weread-bot/main/docs/img/配置.png)
可视化配置界面，支持多种编辑模式，包括基础配置、阅读配置、网络配置、通知配置等，实时同步配置文件。

### 仪表板
![仪表板](https://raw.githubusercontent.com/498330580/weread-bot/main/docs/img/仪表盘.png)
实时监控任务状态、性能指标、统计信息和活动日志，提供完整的运行数据可视化展示。

### 主页
![主页](https://raw.githubusercontent.com/498330580/weread-bot/main/docs/img/主页.png)
Web版本控制面板，支持快速操作（启动任务、停止任务、暂停任务等）和配置文件管理，一站式管理所有功能。

## 快速开始

### 方式一：Web版本（推荐）

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 启动Web服务
```bash
python run.py
# 或直接运行
python app.py
```

#### 3. 访问Web界面
打开浏览器访问：
- 🏠 **主页/仪表板**: http://localhost:5000/
- ⚙️ **配置编辑**: http://localhost:5000/config
- 📊 **详细仪表板**: http://localhost:5000/dashboard

#### 4. 在Web界面中
1. 编辑或上传配置文件
2. 点击"保存配置"
3. 点击"启动任务"按钮开始阅读

### 方式二：命令行版本

如需使用原始命令行版本，请参考项目早期版本。

### 方式三：Docker部署

详见 [部署方式](#部署方式) 章节。

快速命令：
```bash
docker-compose up -d
```

## 项目结构

```
weread-bot/
├── app.py                      # Flask 应用主程序
├── run.py                      # 启动脚本
├── config.yaml                 # 配置文件
├── config.yaml.example         # 配置文件模板
├── requirements.txt            # Python 依赖
├── templates/                  # HTML 模板
│   ├── index.html             # 首页与仪表板
│   ├── config.html            # 配置编辑页面
│   └── dashboard.html         # 详细仪表板页面
├── static/                    # 静态资源（CSS、JS）
├── services/                  # 业务逻辑模块
│   ├── __init__.py
│   ├── config_manager.py      # 配置管理器
│   ├── task_manager.py        # 任务管理器
│   └── log_manager.py         # 日志管理器
├── Dockerfile                 # Docker 镜像配置
├── docker-compose.yml         # Docker Compose 配置
├── .dockerignore              # Docker 忽略文件
├── logs/                      # 日志文件目录
├── README.md                  # 项目文档（本文件）
└── LICENSE                    # MIT 许可证
```

## 配置说明

### 配置管理方式

**Web 界面配置 > 配置文件 > 程序默认值**

Web 服务通过 Web 界面管理所有配置，配置会实时保存到 `config.yaml` 文件中。

### 必需配置

| 配置项 | 描述 |
|--------|------|
| CURL配置 | 微信读书抓包获取的curl命令或文件路径 |

### Web界面覆盖的配置项

通过 http://localhost:5000/config 可以配置：

#### 应用配置
- 启动模式 (immediate/scheduled/daemon)
- 启动延迟 (秒)

#### CURL配置
- 单用户模式（文件路径编辑）
- 多用户模式（多个用户配置）

#### 阅读配置
- 阅读模式 (smart_random/sequential/pure_random)
- 目标阅读时长（分钟）
- 阅读间隔（秒）
- 智能随机参数（书籍连续性、章节连续性、换书冷却）
- 书籍和章节配置

#### 人类行为模拟
- 启用/禁用行为模拟
- 阅读速度变化
- 中途休息概率和时长

#### 网络配置
- 请求超时
- 重试次数
- 重试延迟
- 请求频率限制

#### 通知配置
- 12个通知通道配置（PushPlus、Telegram、Bark等）
- 通知启用/禁用
- 测试通知功能

#### 定时任务配置
- Cron表达式
- 时区设置

#### 守护进程配置
- 会话间隔
- 每日最大会话数

### 配置文件示例

当前配置会自动使用提供的默认值。想了解每个配置项的详细信息，请查看 `config.yaml.example` 文件。

### 多用户配置

```
curl_config:
  users:
    - name: "用户1"
      file_path: "user1_curl.txt"
      reading_overrides:
        target_duration: "45-90"
        mode: "smart_random"
    - name: "用户2"
      file_path: "user2_curl.txt"
      reading_overrides:
        target_duration: "30-60"
        mode: "sequential"
```

### 通知服务配置

| 服务 | 环境变量 | 说明 |
|------|----------|------|
| PushPlus | `PUSHPLUS_TOKEN` | PushPlus推送token |
| Telegram | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | Telegram机器人token和聊天ID |
| WxPusher | `WXPUSHER_SPT` | WxPusher SPT |
| Bark | `BARK_SERVER`, `BARK_DEVICE_KEY`, `BARK_SOUND` | Bark推送服务配置 |
| Ntfy | `NTFY_SERVER`, `NTFY_TOPIC`, `NTFY_TOKEN` | Ntfy服务配置 |
| 飞书 | `FEISHU_WEBHOOK_URL`, `FEISHU_MSG_TYPE` | 飞书Webhook配置 |
| 企业微信 | `WEWORK_WEBHOOK_URL`, `WEWORK_MSG_TYPE` | 企业微信Webhook配置 |
| 钉钉 | `DINGTALK_WEBHOOK_URL`, `DINGTALK_MSG_TYPE` | 钉钉Webhook配置 |
| Gotify | `GOTIFY_SERVER`, `GOTIFY_TOKEN`, `GOTIFY_PRIORITY` | Gotify服务配置 |
| Server酱³ | `SERVERCHAN3_UID`, `SERVERCHAN3_SENDKEY` | Server酱³配置 |
| PushDeer | `PUSHDEER_PUSHKEY`, `PUSHDEER_TYPE` | PushDeer配置 |
| Apprise | `APPRISE_URL` | Apprise通知URL |

## 运行模式

### 1. 立即执行模式 (immediate)
```bash
python weread-bot.py
# 或
python weread-bot.py --mode immediate
```
- 启动后立即开始一次阅读会话
- 完成目标时长后自动退出
- 适合单次使用或手动控制

### 2. 定时执行模式 (scheduled)
```bash
python weread-bot.py --mode scheduled
```
配置：
```yaml
schedule:
  enabled: true
  cron_expression: "0 */2 * * *"    # 每2小时执行一次
  timezone: "Asia/Shanghai"
```

Cron表达式示例：
- `"0 */2 * * *"` - 每2小时执行一次
- `"30 9 * * *"` - 每天9:30执行
- `"0 9,18 * * *"` - 每天9点和18点执行
- `"0 8,12,18 * * *"` - 每天8:00、12:00、18:00执行

### 3. 守护进程模式 (daemon)
```bash
python weread-bot.py --mode daemon
```
配置：
```yaml
daemon:
  enabled: true
  session_interval: "120-180"       # 会话间隔（分钟）
  max_daily_sessions: 12            # 每天最多会话数
```

## 阅读模式

### 智能随机模式 (smart_random) ⭐推荐
```yaml
reading:
  mode: "smart_random"
  smart_random:
    book_continuity: 0.8          # 继续当前书籍的概率
    chapter_continuity: 0.7       # 顺序阅读章节的概率
    book_switch_cooldown: 300     # 换书冷却时间（秒）
```

### 顺序阅读模式 (sequential)
按配置的书籍和章节顺序依次阅读

### 纯随机模式 (pure_random)
完全随机选择书籍和章节

## 部署方式

### 本地开发
```bash
python run.py
```

### Docker 单容器
```bash
docker build -t weread-bot-web .
docker run -p 5000:5000 weread-bot-web
```

### Docker Compose
```bash
docker-compose up -d
```

### 生产部署 (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 修改端口

```bash
# Docker 重新映射
docker run -p 8080:5000 weread-bot-web

# Gunicorn
gunicorn -b 0.0.0.0:8080 app:app
```

## REST API 接口

### 配置管理
```bash
# 获取配置
curl http://localhost:5000/api/config

# 保存配置
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{...配置内容...}'

# 导出配置
curl http://localhost:5000/api/export/config > config.yaml

# 导入配置
curl -X POST -F "file=@config.yaml" http://localhost:5000/api/import/config
```

### 任务控制
```bash
# 启动任务
curl -X POST http://localhost:5000/api/task/start

# 停止任务
curl -X POST http://localhost:5000/api/task/stop

# 获取任务状态
curl http://localhost:5000/api/task/status
```

### 日志管理
```bash
# 获取日志
curl "http://localhost:5000/api/logs?limit=100"

# 清空日志
curl -X POST http://localhost:5000/api/logs/clear

# 下载日志
curl http://localhost:5000/api/logs/download > logs.txt
```

### 健康检查
```bash
curl http://localhost:5000/api/health
```

## 抓包配置详解

### 获取CURL命令步骤

1. 打开微信读书网页版：https://weread.qq.com/
2. 登录账号
3. 找一本书开始阅读
4. 按F12打开开发者工具
5. 在Network标签中翻页，查找 `https://weread.qq.com/web/book/read` 请求
6. 右键请求 → Copy → Copy as cURL (bash)
7. 将CURL命令保存到文件或环境变量

### 配置方式

**方式1：直接CURL字符串**
```bash
# 在Web界面的CURL配置中粘贴：
curl 'https://weread.qq.com/web/book/read' -H 'cookie: wr_skey=...' --data-raw '{...}'
```

**方式2：保存到文件**
```bash
# 将curl命令保存到curl_command.txt文件
echo "curl '...' " > curl_command.txt
# 然后在Web界面加载
```

**方式3：在Web界面编辑**
访问 http://localhost:5000/config → 点击编辑CURL按鈕

## 常见问题

### Q: 启动时缺少依赖
**A:** 运行 `pip install -r requirements.txt`

### Q: 端口5000已被占用
**A:** 修改run.py中的port值为你需要的端口号（默认5000）

### Q: 无法访问Web界面
**A:** 
- 检查防火墙设置
- 确保Flask服务正在运行
- 查看控制台输出错误信息

### Q: 任务无法启动
**A:**
- 检查 `logs/weread.log` 日志文件
- 验证CURL命令是否有效
- 确保微信读书账号未过期

### Q: 如何防止被识别为机器人
**A:** 内置多层防检测机制：
- 启动随机延迟（60-120秒）
- 阅读速度随机变化
- 随机中途休息
- 自动Cookie刷新

### Q: 支持多账号吗
**A:** 支持多用户模式，顺序执行多个账号：
```yaml
curl_config:
  users:
    - name: "账号1"
      file_path: "user1_curl.txt"
    - name: "账号2"
      file_path: "user2_curl.txt"
```

### Q: 程序运行多长时间
**A:** 灵活配置：
- **默认**：60-70分钟随机
- **自定义**：通过 `TARGET_DURATION` 配置
- **守护进程**：可设置每日最大会话数

### Q: 如何查看运行状态
**A:** 多种方式：
- Web界面仪表板
- 日志文件：`logs/weread.log`
- 推送通知（配置后）
- REST API：`/api/task/status`

## 安全建议

1. **保护CURL命令** - 包含个人认证信息
2. **定期更新** - Cookie会过期，需要重新获取
3. **限制访问** - 使用防火墙限制Web服务访问
4. **启用HTTPS** - 在生产环境使用反向代理
5. **适度使用** - 避免过于频繁的阅读行为

## 技术支持

- 📧 提交 Issue：https://github.com/498330580/weread-bot/issues
- 💬 讨论和建议
- 🤝 欢迎贡献代码
- 🌟 如果有帮助，请给个Star！

## 项目信息

| 信息 | 内容 |
|------|------|
| 版本 | 0.3.1 |
| 作者 | 498330580 |
| 仓库 | https://github.com/498330580/weread-bot |
| 许可证 | MIT License |
| Python版本 | 3.10+ |

## 免责声明

本项目仅供学习和研究目的，不得用于任何商业活动。用户在使用本项目时应遵守所在地区的法律法规，对于违法使用所导致的后果，本项目及作者不承担任何责任。

## 致谢

感谢 [funnyzak/weread-bot](https://github.com/funnyzak/weread-bot) 提供思路和部分代码支持。

---

**祝你使用愉快！如有问题欢迎反馈。** 🎉
