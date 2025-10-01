"""
Observe Logging Integration for Bird Feeding API
Provides structured logging, metrics, and observability features.
"""

import json
import logging
import os
import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps

import requests
import structlog
from pythonjsonlogger import jsonlogger
from flask import request, g, current_app

class ObserveLogger:
    """Observe.inc integration for Flask applications"""
    
    def __init__(self, app=None, config_file='config/observe_config.json'):
        self.app = app
        self.config = {}
        self.session = requests.Session()
        self.enabled = False
        
        if app is not None:
            self.init_app(app, config_file)
    
    def init_app(self, app, config_file='config/observe_config.json'):
        """Initialize Observe logging with Flask app"""
        self.app = app
        self.load_config(config_file)
        
        if self.config.get('observe', {}).get('enabled', False):
            self.enabled = True
            self.setup_logging()
            self.setup_request_middleware()
            app.logger.info("🔍 Observe logging initialized successfully")
        else:
            app.logger.info("⚠️ Observe logging disabled in configuration")
    
    def load_config(self, config_file):
        """Load Observe configuration from file or Nexus"""
        try:
            # Try local file first
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
                return
            
            # Fallback: Try to fetch from Nexus
            nexus_url = f"http://localhost:8081/repository/test-raw/{config_file}"
            try:
                response = requests.get(nexus_url, auth=('admin', 'admin123'))
                if response.status_code == 200:
                    self.config = response.json()
                    print("📦 Loaded Observe config from Nexus Repository!")
                    return
            except Exception as e:
                print(f"Warning: Could not fetch Observe config from Nexus: {e}")
            
            # Default configuration
            self.config = {
                "observe": {"enabled": False},
                "logging": {"format": "json"}
            }
            
        except Exception as e:
            print(f"Warning: Could not load Observe config: {e}")
            self.config = {"observe": {"enabled": False}}
    
    def setup_logging(self):
        """Configure structured logging"""
        log_format = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "module": "%(module)s"}'
        )
        
        # Configure Flask app logger
        handler = logging.StreamHandler()
        handler.setFormatter(log_format)
        self.app.logger.addHandler(handler)
        self.app.logger.setLevel(getattr(logging, self.config['observe'].get('log_level', 'INFO')))
    
    def setup_request_middleware(self):
        """Set up request/response middleware for observability"""
        
        @self.app.before_request
        def before_request():
            g.request_id = str(uuid.uuid4())
            g.start_time = time.time()
            
            self.log_request_start()
        
        @self.app.after_request
        def after_request(response):
            self.log_request_end(response)
            return response
    
    def log_request_start(self):
        """Log incoming request details"""
        if not self.enabled:
            return
        
        log_data = {
            "event_type": "http_request_start",
            "request_id": g.request_id,
            "method": request.method,
            "path": request.path,
            "user_agent": request.headers.get('User-Agent', ''),
            "remote_addr": request.remote_addr,
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.config['observe'].get('service_name', 'bird-feeding-api')
        }
        
        self.send_to_observe(log_data)
    
    def log_request_end(self, response):
        """Log request completion details"""
        if not self.enabled:
            return
        
        duration = time.time() - g.start_time
        
        log_data = {
            "event_type": "http_request_end",
            "request_id": g.request_id,
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "response_size": self._get_response_size(response),
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.config['observe'].get('service_name', 'bird-feeding-api')
        }
        
        self.send_to_observe(log_data)

    def _get_response_size(self, response):
        """Safely get response size, handling static files and streaming responses"""
        try:
            if hasattr(response, 'content_length') and response.content_length:
                return response.content_length
            elif hasattr(response, 'get_data'):
                return len(response.get_data())
        except (RuntimeError, AttributeError):
            # Handle direct passthrough mode for static files
            pass
        return 0

    def log_business_event(self, event_type: str, data: Dict[str, Any], level: str = "INFO"):
        """Log business logic events"""
        if not self.enabled:
            return
        
        log_data = {
            "event_type": event_type,
            "request_id": getattr(g, 'request_id', 'no-request'),
            "level": level,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.config['observe'].get('service_name', 'bird-feeding-api')
        }
        
        self.send_to_observe(log_data)
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log errors with context"""
        if not self.enabled:
            return
        
        log_data = {
            "event_type": "error",
            "request_id": getattr(g, 'request_id', 'no-request'),
            "level": "ERROR",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.config['observe'].get('service_name', 'bird-feeding-api')
        }
        
        self.send_to_observe(log_data)
    
    def send_to_observe(self, log_data: Dict[str, Any]):
        """Send log data to Observe.inc"""
        if not self.enabled:
            return
        
        try:
            # For demo purposes, we'll log to console
            # In production, you'd send to Observe's collect endpoint
            observe_config = self.config['observe']
            
            # Add standard fields
            log_data.update({
                "customer_id": observe_config.get('customer_id', 'demo'),
                "environment": observe_config.get('environment', 'development'),
            })
            
            # In a real implementation, you'd POST to Observe
            # requests.post(observe_config['collect_url'], json=log_data, headers={...})
            
            # For now, structured logging to console
            print(f"📊 OBSERVE: {json.dumps(log_data, indent=2)}")
            
        except Exception as e:
            print(f"Error sending to Observe: {e}")

def observe_track(event_type: str, include_args: bool = True):
    """Decorator to automatically track function calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Log successful execution
                if hasattr(current_app, 'observe_logger'):
                    data = {
                        "function": func.__name__,
                        "duration_ms": round((time.time() - start_time) * 1000, 2),
                        "success": True
                    }
                    
                    if include_args and kwargs:
                        # Filter out sensitive data
                        safe_kwargs = {k: v for k, v in kwargs.items() 
                                     if k not in ['password', 'token', 'api_key']}
                        data["arguments"] = safe_kwargs
                    
                    current_app.observe_logger.log_business_event(event_type, data)
                
                return result
                
            except Exception as e:
                # Log error
                if hasattr(current_app, 'observe_logger'):
                    current_app.observe_logger.log_error(e, {
                        "function": func.__name__,
                        "duration_ms": round((time.time() - start_time) * 1000, 2)
                    })
                raise
        
        return wrapper
    return decorator
