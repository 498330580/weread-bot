#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日志管理服务"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from logging.handlers import RotatingFileHandler


class LogManager:
    """日志管理器"""
    
    def __init__(self, log_file: str = "logs/weread.log"):
        self.log_file = log_file
        self.logs = []
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        # 创建日志目录
        Path(self.log_file).parent.mkdir(exist_ok=True)
        
        logger = logging.getLogger('weread_bot')
        logger.setLevel(logging.DEBUG)
        
        # 移除现有的处理器，避免重复
        logger.handlers.clear()
        
        # 文件处理器
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log(self, level: str, message: str, **kwargs):
        """记录日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level.upper(),
            'message': message,
            'data': kwargs
        }
        
        self.logs.append(log_entry)
        
        # 限制内存中的日志数量
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]
        
        # 同时写入系统日志
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)
    
    def debug(self, message: str, **kwargs):
        """记录调试日志"""
        self.log('debug', message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """记录信息日志"""
        self.log('info', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """记录警告日志"""
        self.log('warning', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """记录错误日志"""
        self.log('error', message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """记录严重错误日志"""
        self.log('critical', message, **kwargs)
    
    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取日志"""
        return self.logs[-limit:]
    
    def clear_logs(self):
        """清空日志"""
        self.logs = []
        self.info("日志已清空")
    
    def get_log_file_content(self) -> str:
        """获取日志文件内容"""
        try:
            if Path(self.log_file).exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            return f"读取日志文件失败: {e}"
