#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""配置管理服务"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Web版本的配置管理器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"配置文件加载失败: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'app': {
                'name': 'WeReadBot',
                'version': '1.0.5',
                'startup_mode': 'immediate',
                'startup_delay': '1-10'
            },
            'curl_config': {
                'file_path': 'curl_command.txt'
            },
            'reading': {
                'mode': 'smart_random',
                'target_duration': '60-70',
                'reading_interval': '25-35',
                'use_curl_data_first': True,
                'fallback_to_config': True,
                'books': [],
                'smart_random': {
                    'book_continuity': 0.8,
                    'chapter_continuity': 0.7,
                    'book_switch_cooldown': 300
                }
            },
            'human_simulation': {
                'enabled': True,
                'reading_speed_variation': True,
                'break_probability': 0.15,
                'break_duration': '30-180',
                'rotate_user_agent': False
            },
            'network': {
                'timeout': 30,
                'retry_times': 3,
                'retry_delay': '5-15',
                'rate_limit': 10
            },
            'notification': {
                'enabled': True,
                'include_statistics': True,
                'channels': []
            },
            'hack': {
                'cookie_refresh_ql': False
            },
            'schedule': {
                'enabled': False,
                'cron_expression': '0 */2 * * *',
                'timezone': 'Asia/Shanghai'
            },
            'daemon': {
                'enabled': False,
                'session_interval': '120-180',
                'max_daily_sessions': 12
            },
            'logging': {
                'level': 'INFO',
                'format': 'detailed',
                'file': 'logs/weread.log',
                'max_size': '10MB',
                'backup_count': 5,
                'console': True
            }
        }
    
    def get_config_dict(self) -> Dict[str, Any]:
        """获取配置字典"""
        return self.config
    
    def save_config(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """保存配置到文件"""
        try:
            # 保存到YAML文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            
            # 更新内存中的配置
            self.config = config_dict
            
            return {
                'success': True,
                'message': '配置已保存',
                'path': self.config_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_config_value(self, path: str, default: Any = None) -> Any:
        """获取配置值（支持点号路径）"""
        keys = path.split('.')
        current = self.config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def set_config_value(self, path: str, value: Any) -> bool:
        """设置配置值（支持点号路径）"""
        keys = path.split('.')
        current = self.config
        
        # 遍历到倒数第二个键
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # 设置最后的键
        current[keys[-1]] = value
        
        # 保存到文件
        result = self.save_config(self.config)
        return result.get('success', False)
    
    def reload_config(self) -> bool:
        """重新加载配置文件"""
        try:
            self.config = self._load_config()
            return True
        except Exception as e:
            print(f"重新加载配置失败: {e}")
            return False
    
    def reset_config(self) -> Dict[str, Any]:
        """重置为默认配置"""
        self.config = self._get_default_config()
        result = self.save_config(self.config)
        return self.config
    
    def merge_config(self, partial_config: Dict[str, Any]) -> bool:
        """合并配置"""
        def deep_merge(base, updates):
            for key, value in updates.items():
                if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
        
        try:
            deep_merge(self.config, partial_config)
            result = self.save_config(self.config)
            return result.get('success', False)
        except Exception as e:
            print(f"合并配置失败: {e}")
            return False
