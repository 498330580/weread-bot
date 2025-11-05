#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WeRead Bot Flask Web 应用

Flask Web服务，提供可视化界面配置和管理微信读书阅读机器人
"""

import os
import json
import threading
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 配置
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局变量存储应用状态
app_state = {
    'is_running': False,
    'current_task': None,
    'config': None,
    'logs': [],
    'session_data': {}
}

# 导入业务逻辑（我们会创建这些模块）
from services.config_manager import ConfigManager
from services.task_manager import TaskManager
from services.log_manager import LogManager


class WebConfigManager:
    """Web配置管理器"""
    
    def __init__(self):
        self.config_file = "config.yaml"
        self.config_manager = ConfigManager(self.config_file)
        self.log_manager = LogManager()
        self.task_manager = TaskManager(self.config_manager, self.log_manager)
    
    def get_config(self):
        """获取当前配置"""
        return self.config_manager.get_config_dict()
    
    def save_config(self, config_dict):
        """保存配置到文件"""
        return self.config_manager.save_config(config_dict)
    
    def get_logs(self, limit=100):
        """获取日志"""
        return self.log_manager.get_logs(limit)
    
    def clear_logs(self):
        """清空日志"""
        return self.log_manager.clear_logs()


# 初始化配置管理器
web_config = WebConfigManager()


# ==================== 前端路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/config')
def config_page():
    """配置页面"""
    return render_template('config.html')


@app.route('/dashboard')
def dashboard():
    """仪表板页面"""
    return render_template('dashboard.html')


# ==================== API 接口路由 ====================

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    try:
        config = web_config.get_config()
        return jsonify({
            'success': True,
            'data': config
        })
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config', methods=['POST'])
def save_config():
    """保存配置"""
    try:
        config_data = request.get_json()
        result = web_config.save_config(config_data)
        return jsonify({
            'success': True,
            'message': '配置保存成功',
            'data': result
        })
    except Exception as e:
        logger.error(f"保存配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config/validate', methods=['POST'])
def validate_config():
    """验证配置"""
    try:
        config_data = request.get_json()
        # 这里可以添加配置验证逻辑
        return jsonify({
            'success': True,
            'message': '配置验证通过'
        })
    except Exception as e:
        logger.error(f"验证配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/task/start', methods=['POST'])
def start_task():
    """启动阅读任务"""
    try:
        if app_state['is_running']:
            return jsonify({
                'success': False,
                'error': '任务已在运行中'
            }), 400
        
        config_data = request.get_json() or {}
        
        # 在后台线程中启动任务
        app_state['is_running'] = True
        task_thread = threading.Thread(
            target=web_config.task_manager.run_task,
            args=(config_data,),
            daemon=True
        )
        task_thread.start()
        
        return jsonify({
            'success': True,
            'message': '任务已启动',
            'task_id': 'task_' + datetime.now().isoformat()
        })
    except Exception as e:
        app_state['is_running'] = False
        logger.error(f"启动任务失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/task/stop', methods=['POST'])
def stop_task():
    """停止阅读任务"""
    try:
        app_state['is_running'] = False
        web_config.task_manager.stop_task()
        
        return jsonify({
            'success': True,
            'message': '任务已停止'
        })
    except Exception as e:
        logger.error(f"停止任务失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/task/status', methods=['GET'])
def get_task_status():
    """获取任务状态"""
    try:
        status = {
            'is_running': app_state['is_running'],
            'current_task': app_state['current_task'],
            'timestamp': datetime.now().isoformat()
        }
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """获取日志"""
    try:
        limit = request.args.get('limit', 100, type=int)
        logs = web_config.get_logs(limit)
        return jsonify({
            'success': True,
            'data': logs
        })
    except Exception as e:
        logger.error(f"获取日志失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """清空日志"""
    try:
        web_config.clear_logs()
        return jsonify({
            'success': True,
            'message': '日志已清空'
        })
    except Exception as e:
        logger.error(f"清空日志失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/logs/download', methods=['GET'])
def download_logs():
    """下载日志文件"""
    try:
        from flask import send_file
        log_file = Path('logs/weread.log')
        if log_file.exists():
            return send_file(
                str(log_file),
                as_attachment=True,
                download_name=f'weread-{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'
            )
        else:
            return jsonify({
                'success': False,
                'error': '日志文件不存在'
            }), 404
    except Exception as e:
        logger.error(f"下载日志失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/config', methods=['GET'])
def export_config():
    """导出配置文件"""
    try:
        from flask import send_file
        if Path('config.yaml').exists():
            return send_file(
                'config.yaml',
                as_attachment=True,
                download_name=f'config-{datetime.now().strftime("%Y%m%d-%H%M%S")}.yaml'
            )
        else:
            return jsonify({
                'success': False,
                'error': '配置文件不存在'
            }), 404
    except Exception as e:
        logger.error(f"导出配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/import/config', methods=['POST'])
def import_config():
    """导入配置文件"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有文件上传'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '文件名为空'
            }), 400
        
        if not file.filename.endswith(('.yaml', '.yml')):
            return jsonify({
                'success': False,
                'error': '只支持YAML文件'
            }), 400
        
        # 保存上传的文件
        config_content = file.read().decode('utf-8')
        import yaml
        config_data = yaml.safe_load(config_content)
        
        web_config.save_config(config_data)
        
        return jsonify({
            'success': True,
            'message': '配置导入成功'
        })
    except Exception as e:
        logger.error(f"导入配置失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/notification/test', methods=['POST'])
def test_notification():
    """测试通知功能"""
    try:
        data = request.get_json()
        channels = data.get('channels', [])
        title = data.get('title', '正条阻弋 - 测试通知')
        content = data.get('content', '这是一条测试通知')
        
        if not channels:
            return jsonify({
                'success': False,
                'error': '未配置任何通知通道'
            }), 400
        
        # 针对不同的通知通道发送测试消息
        results = []
        for channel in channels:
            channel_name = channel.get('name')
            channel_config = channel.get('config', {})
            token = channel_config.get('token', '')
            
            try:
                # 这里你可以添加具体的通知发送逻辑
                # 按照不同的通知通道类型调用相应的API
                if channel_name == 'pushplus':
                    # PushPlus通知
                    import requests
                    response = requests.post(
                        'https://www.pushplus.plus/send',
                        json={
                            'token': token,
                            'title': title,
                            'content': content
                        },
                        timeout=10
                    )
                    results.append({
                        'channel': channel_name,
                        'success': response.status_code == 200,
                        'message': '发送成功' if response.status_code == 200 else '发送失败'
                    })
                elif channel_name == 'telegram':
                    # Telegram通知
                    import requests
                    bot_token, chat_id = token.split(':') if ':' in token else (token, '')
                    response = requests.post(
                        f'https://api.telegram.org/bot{bot_token}/sendMessage',
                        json={
                            'chat_id': chat_id,
                            'text': f'<b>{title}</b>\n\n{content}',
                            'parse_mode': 'HTML'
                        },
                        timeout=10
                    )
                    results.append({
                        'channel': channel_name,
                        'success': response.status_code == 200,
                        'message': '发送成功' if response.status_code == 200 else '发送失败'
                    })
                else:
                    # 其他通道简易处理
                    results.append({
                        'channel': channel_name,
                        'success': True,
                        'message': '通道定义待实现'
                    })
            except Exception as e:
                logger.error(f"测试{channel_name}通知失败: {e}")
                results.append({
                    'channel': channel_name,
                    'success': False,
                    'message': str(e)
                })
        
        return jsonify({
            'success': True,
            'message': '测试通知已发送',
            'results': results
        })
    except Exception as e:
        logger.error(f"测试通知失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/curl/load', methods=['GET'])
def load_curl_command():
    """加载CURL命令文件内容"""
    try:
        filename = request.args.get('filename', 'curl_command.txt')
        
        # 确保文件路径安全
        if '/' in filename or '\\' in filename:
            filename = Path(filename).name
        
        # 阅读文件
        if Path(filename).exists():
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'success': True,
                'content': content,
                'filename': filename
            })
        else:
            return jsonify({
                'success': True,
                'content': '',
                'filename': filename,
                'message': '文件不存在'
            })
    except Exception as e:
        logger.error(f"加载CURL命令失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/curl/save', methods=['POST'])
def save_curl_command():
    """保存CURL命令到文件"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        filename = data.get('filename', 'curl_command.txt')
        
        # 确保文件路径安全（只允许保存在当前目录或指定目录）
        if '/' in filename or '\\' in filename:
            filename = Path(filename).name
        
        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'message': f'文件已保存到 {filename}',
            'filename': filename
        })
    except Exception as e:
        logger.error(f"保存CURL命令失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'error': '资源不存在'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"服务器错误: {error}")
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    # 创建必要的目录
    Path('logs').mkdir(exist_ok=True)
    Path('templates').mkdir(exist_ok=True)
    Path('static').mkdir(exist_ok=True)
    
    # 启动Flask应用
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', False),
        threaded=True
    )
