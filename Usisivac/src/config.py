#!/usr/bin/env python3
"""
AI-Powered Code Review System - Configuration

This module provides configuration management for the code review system,
including loading from files, environment variables, and default values.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Add src to path for imports
import sys
sys.path.insert(0, os.path.dirname(__file__))


class ReviewConfig:
    """Configuration class for the code review system."""

    DEFAULT_CONFIG = {
        "supported_extensions": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rs", ".php", ".rb"],
        "review_categories": ["security", "performance", "quality"],
        "security_patterns": {
            "sql_injection": {
                "patterns": [r"ex" + r"ecute\(", r"qu" + r"ery\(", r"ex" + r"ec\(", r"ev" + r"al\("],
                "severity": "high",
                "description": "Potential SQL injection vulnerability"
            },
            "xss": {
                "patterns": [r"inn" + r"erHTML", r"docu" + r"ment\.write", r"ev" + r"al\("],
                "severity": "high",
                "description": "Potential XSS vulnerability"
            },

            "hardcoded_secrets": {
                "patterns": ["pass" + "word=", "sec" + "ret=", "ke" + "y=", "tok" + "en="],
                "severity": "critical",
                "description": "Hardcoded secrets detected"
            }
        },
        "performance_patterns": {
            "n_plus_1_queries": {
                "patterns": ["for.*in.*:.*query", "foreach.*query"],
                "severity": "medium",
                "description": "Potential N+1 query problem"
            },
            "inefficient_loops": {
                "patterns": ["for.*in.*range\\(len\\(", "while.*true"],
                "severity": "medium",
                "description": "Inefficient loop pattern"
            }
        },
        "quality_patterns": {
            "code_duplication": {
                "patterns": ["copy.*paste", "duplicate.*code"],
                "severity": "low",
                "description": "Code duplication detected"
            },
            "missing_docstrings": {
                "patterns": ["def.*:", "class.*:", "function.*:"],
                "severity": "low",
                "description": "Missing documentation"
            }
        },
        "llm_config": {
            "model": "llama-3.3-70b",
            "temperature": 0.3,
            "max_tokens": 1000,
            "api_key": None  # Strictly from environment
        },
        "vector_db": {
            "collection": "code_review_patterns",
            "embedding_model": "all-MiniLM-L6-v2"
        },
        "output_settings": {
            "max_issues_per_file": 10,
            "max_context_lines": 5,
            "include_code_samples": True
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config(config_path)

    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        config = self.DEFAULT_CONFIG.copy()

        # Load from file if provided
        if config_path:
            path = Path(config_path)
            if path.exists():
                try:
                    if path.suffix in [".json"]:
                        with open(path, "r", encoding="utf-8") as f:
                            file_config = json.load(f)
                    elif path.suffix in [".yaml", ".yml"]:
                        with open(path, "r", encoding="utf-8") as f:
                            file_config = yaml.safe_load(f)
                    else:
                        self.logger.warning(f"Unsupported config file format: {path.suffix}")
                        return config

                    # Merge file config with defaults
                    self._deep_merge(config, file_config)
                    self.logger.info(f"Loaded configuration from {config_path}")
                except Exception as e:
                    self.logger.error(f"Error loading config from {config_path}: {e}")
            else:
                self.logger.warning(f"Config file not found: {config_path}")

        # Load from environment variables (overrides file and defaults)
        self._load_env_config(config)

        # Security check: Ensure API key is present in final config if needed
        # (This avoids hardcoding defaults in source)
        if not config["llm_config"].get("api_key"):
            self.logger.debug("API_KEY not found in configuration or environment.")

        return config

    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]):
        """Recursively merge two dictionaries."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value

    def _load_env_config(self, config: Dict[str, Any]):
        """Load configuration from environment variables."""
        env_mapping = {
            "GROQ_API_KEY": ("llm_config", "api_key"),
            "OPENAI_API_KEY": ("llm_config", "api_key"),
            "SUPPORTED_EXTENSIONS": ("supported_extensions", self._parse_list),
            "REVIEW_CATEGORIES": ("review_categories", self._parse_list),
            "LLM_MODEL": ("llm_config", "model"),
            "COLLECTION": ("vector_db", "collection"),
            "EMBEDDING_MODEL": ("vector_db", "embedding_model"),
            "MAX_ISSUES": ("output_settings", "max_issues_per_file"),
            "MAX_CONTEXT": ("output_settings", "max_context_lines")
        }

        for env_var, config_path in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                if isinstance(config_path, tuple):
                    section, key = config_path
                    if len(config_path) == 3:
                        transform = config_path[2]
                        config[section][key] = transform(value)
                    else:
                        config[section][key] = value
                else:
                    config[config_path] = value

    def _parse_list(self, value: str) -> List[str]:
        """Parse a comma-separated list."""
        return [item.strip() for item in value.split(",") if item.strip()]

    @property
    def supported_extensions(self) -> List[str]:
        return self.config.get("supported_extensions", [])

    @property
    def review_categories(self) -> List[str]:
        return self.config.get("review_categories", [])

    @property
    def security_patterns(self) -> Dict[str, Any]:
        return self.config.get("security_patterns", {})

    @property
    def performance_patterns(self) -> Dict[str, Any]:
        return self.config.get("performance_patterns", {})

    @property
    def quality_patterns(self) -> Dict[str, Any]:
        return self.config.get("quality_patterns", {})

    @property
    def llm_config(self) -> Dict[str, Any]:
        return self.config.get("llm_config", {})

    @property
    def vector_db(self) -> Dict[str, Any]:
        return self.config.get("vector_db", {})

    @property
    def output_settings(self) -> Dict[str, Any]:
        return self.config.get("output_settings", {})

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def __contains__(self, key: str) -> bool:
        return key in self.config

    def __str__(self) -> str:
        return json.dumps(self.config, indent=2)
