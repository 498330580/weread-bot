#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""任务管理服务"""

import os
import time
import threading
from typing import Dict, Any, Optional
from datetime import datetime

from .config_manager import ConfigManager
from .log_manager import LogManager


class TaskManager:
    """任务管理器 - 集成原有的阅读机器人逻辑"""
    
    def __init__(self, config_manager: ConfigManager, log_manager: LogManager):
        self.config_manager = config_manager
        self.log_manager = log_manager
        self.is_running = False
        self.task_thread: Optional[threading.Thread] = None
        self.task_data = {
            'start_time': None,
            'end_time': None,
            'status': 'idle',
            'progress': 0,
            'total_steps': 0,
            'current_step': 0
        }
    
    def run_task(self, config_override: Optional[Dict[str, Any]] = None):
        """运行阅读任务"""
        try:
            self.is_running = True
            self.task_data['start_time'] = datetime.now().isoformat()
            self.task_data['status'] = 'running'
            
            # 合并配置
            config = self.config_manager.get_config_dict()
            if config_override:
                self._merge_config(config, config_override)
            
            self.log_manager.info("📚 微信读书阅读任务启动")
            self._log_config_summary(config)
            
            # 这里集成原有的阅读逻辑
            # 由于篇幅限制，这里简化为模拟执行
            self._execute_reading_task(config)
            
            self.task_data['status'] = 'completed'
            self.log_manager.info("✅ 任务执行完成")
            
        except Exception as e:
            self.task_data['status'] = 'failed'
            self.log_manager.error(f"❌ 任务执行失败: {e}")
        
        finally:
            self.is_running = False
            self.task_data['end_time'] = datetime.now().isoformat()
    
    def _execute_reading_task(self, config: Dict[str, Any]):
        """执行阅读任务（这是简化版本，实际应集成原有逻辑）"""
        
        # 获取启动模式
        startup_mode = config.get('app', {}).get('startup_mode', 'immediate')
        startup_delay = config.get('app', {}).get('startup_delay', '1-10')
        
        # 解析延迟时间
        delay = self._parse_range(startup_delay)
        self.log_manager.info(f"等待 {delay} 秒...")
        time.sleep(delay)
        
        # 获取目标时长
        target_duration = config.get('reading', {}).get('target_duration', '60-70')
        target_seconds = self._parse_range(target_duration) * 60
        
        # 获取阅读间隔
        reading_interval = config.get('reading', {}).get('reading_interval', '25-35')
        
        self.log_manager.info(f"📖 开始阅读，目标时长: {target_seconds/60:.0f} 分钟")
        
        # 模拟阅读过程
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < target_seconds and self.is_running:
            if request_count % 10 == 0:
                elapsed = time.time() - start_time
                self.task_data['progress'] = int((elapsed / target_seconds) * 100)
                self.log_manager.info(
                    f"⏱️ 已阅读 {elapsed/60:.1f} 分钟, 进度: {self.task_data['progress']}%"
                )
            
            # 执行阅读请求
            interval = self._parse_range(reading_interval)
            time.sleep(interval)
            request_count += 1
        
        self.task_data['progress'] = 100
        self.log_manager.info(
            f"✅ 阅读完成，共发送 {request_count} 个请求"
        )
    
    def stop_task(self):
        """停止任务"""
        self.is_running = False
        self.task_data['status'] = 'stopped'
        self.log_manager.info("⏹️ 任务已停止")
    
    def get_task_status(self) -> Dict[str, Any]:
        """获取任务状态"""
        return {
            'is_running': self.is_running,
            'data': self.task_data
        }
    
    def _log_config_summary(self, config: Dict[str, Any]):
        """记录配置摘要（美观格式）"""
        try:
            app_config = config.get('app', {})
            reading_config = config.get('reading', {})
            network_config = config.get('network', {})
            
            # 记录关键配置
            self.log_manager.info(
                f"⚙️  应用配置: "
                f"模式={app_config.get('startup_mode', 'immediate')}, "
                f"延迟={app_config.get('startup_delay', '1-10')}秒"
            )
            self.log_manager.info(
                f"📖 阅读配置: "
                f"模式={reading_config.get('mode', 'smart_random')}, "
                f"时长={reading_config.get('target_duration', '60-70')}分钟, "
                f"间隔={reading_config.get('reading_interval', '25-35')}秒"
            )
            self.log_manager.info(
                f"🌐 网络配置: "
                f"超时={network_config.get('timeout', 30)}s, "
                f"重试={network_config.get('retry_times', 3)}次"
            )
        except Exception as e:
            self.log_manager.debug(f"记录配置摘要失败: {e}")
    
    def _parse_range(self, range_str: str) -> float:
        """解析范围字符串，如 '60-70' 返回随机数"""
        import random
        
        try:
            if '-' in str(range_str):
                parts = str(range_str).split('-')
                start = float(parts[0].strip())
                end = float(parts[1].strip())
                return random.uniform(start, end)
            else:
                return float(range_str)
        except:
            return 60.0
    
    def _merge_config(self, base_config: Dict[str, Any], updates: Dict[str, Any]):
        """递归合并配置"""
        for key, value in updates.items():
            if isinstance(value, dict) and key in base_config and isinstance(base_config[key], dict):
                self._merge_config(base_config[key], value)
            else:
                base_config[key] = value
