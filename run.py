#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeRead Bot Flask Web 应用启动脚本

这是一个启动脚本，可以直接运行来启动Flask应用
"""

import os
import sys
from pathlib import Path

# 确保必要的目录存在
Path('logs').mkdir(exist_ok=True)
Path('templates').mkdir(exist_ok=True)
Path('static').mkdir(exist_ok=True)
Path('services').mkdir(exist_ok=True)

# 检查依赖
try:
    import flask
    import flask_cors
    import yaml
except ImportError:
    print("❌ 缺少必要的依赖，请运行: pip install -r requirements.txt")
    sys.exit(1)

# 导入应用
try:
    from app import app
    
    if __name__ == '__main__':
        # 从环境变量或默认值获取配置
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        port = int(os.getenv('FLASK_PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
        
        print(f"""
╔════════════════════════════════════════════════════╗
║         WeRead Bot - Web版微信读书机器人           ║
╚════════════════════════════════════════════════════╝

🚀 Flask服务启动中...

📝 配置信息:
   • 地址: http://{host}:{port}
   • 调试模式: {'开启 🐛' if debug else '关闭'}
   • 日志: logs/weread.log
   • 配置文件: config.yaml

🌐 访问地址:
   • 主页: http://localhost:{port}/
   • 仪表板: http://localhost:{port}/dashboard
   • 配置: http://localhost:{port}/config
   • API: http://localhost:{port}/api/health

⚠️  按 Ctrl+C 停止服务

═══════════════════════════════════════════════════════
        """)
        
        # 启动应用
        app.run(host=host, port=port, debug=debug, threaded=True)
        
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保所有依赖已安装: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ 启动失败: {e}")
    sys.exit(1)
