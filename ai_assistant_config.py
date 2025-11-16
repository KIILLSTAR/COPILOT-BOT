#!/usr/bin/env python3
"""
AI Assistant Configuration
Allows you to enable/disable features and customize behavior
"""
import os
import json
from typing import Dict, Any, Optional

class AIAssistantConfig:
    """
    Configuration for AI Trading Assistant
    Allows you to use AI assistant standalone or with autonomous bot
    """
    
    # Default configuration file path
    CONFIG_FILE = "ai_assistant_config.json"
    
    # Default settings
    DEFAULT_CONFIG = {
        # Autonomous bot settings
        "autonomous_bot_enabled": False,  # Enable/disable autonomous trading bot
        "bot_auto_trade": False,          # Bot can execute trades automatically
        
        # AI Assistant settings
        "ai_assistant_enabled": True,     # Enable AI assistant (works standalone)
        "ai_auto_refresh": False,         # Auto-refresh AI recommendations
        "ai_refresh_interval": 60,        # Seconds between auto-refresh
        
        # Data sources
        "primary_data_source": "jupiter", # "jupiter" or "fallback"
        "use_jupiter_perps": True,        # Pull directly from Jupiter perps API
        "use_bot_data": False,            # Use bot's market data (if bot is running)
        
        # Ollama settings
        "ollama_url": None,               # Auto-detect from env or use default
        "ollama_model": "llama3.2",       # Model to use
        
        # Display settings
        "show_detailed_analysis": True,   # Show full analysis or brief summary
        "alert_on_high_confidence": True, # Alert when confidence >= 8
        "high_confidence_threshold": 8,   # Confidence threshold for alerts
        
        # Comet ML (optional)
        "comet_enabled": False,           # Enable Comet ML tracking
        "comet_api_key": None,            # Set via env: COMET_API_KEY
        
        # Trading integration
        "integrate_with_bot": False,      # Show AI recommendations in bot cycles
        "standalone_mode": True,          # Works without bot infrastructure
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration"""
        self.config_file = config_file or self.CONFIG_FILE
        self.config = self._load_config()
        self._apply_environment_overrides()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle missing keys
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded)
                    return config
            except Exception as e:
                print(f"⚠️ Error loading config: {e}, using defaults")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self._save_config(self.DEFAULT_CONFIG.copy())
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Optional[Dict[str, Any]] = None):
        """Save configuration to file"""
        config = config or self.config
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving config: {e}")
    
    def _apply_environment_overrides(self):
        """Apply environment variable overrides"""
        # Ollama settings
        if os.getenv('OLLAMA_URL'):
            self.config['ollama_url'] = os.getenv('OLLAMA_URL')
        if os.getenv('OLLAMA_CLOUD_URL'):
            self.config['ollama_url'] = os.getenv('OLLAMA_CLOUD_URL')
        if os.getenv('OLLAMA_MODEL'):
            self.config['ollama_model'] = os.getenv('OLLAMA_MODEL')
        
        # Comet settings
        if os.getenv('COMET_API_KEY'):
            self.config['comet_enabled'] = True
            self.config['comet_api_key'] = os.getenv('COMET_API_KEY')
        
        # Auto-detect standalone mode if bot components unavailable
        try:
            from core.simulation_engine import simulator
            # Bot components available
            self.config['standalone_mode'] = False
        except ImportError:
            # Bot components not available - force standalone
            self.config['standalone_mode'] = True
            self.config['integrate_with_bot'] = False
            self.config['use_bot_data'] = False
    
    def get(self, key: str, default: Any = None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any, save: bool = True):
        """Set configuration value"""
        self.config[key] = value
        if save:
            self._save_config()
    
    def update(self, updates: Dict[str, Any], save: bool = True):
        """Update multiple configuration values"""
        self.config.update(updates)
        if save:
            self._save_config()
    
    def enable_standalone_mode(self):
        """Enable standalone mode (works without bot)"""
        self.update({
            'standalone_mode': True,
            'integrate_with_bot': False,
            'autonomous_bot_enabled': False,
            'use_bot_data': False,
            'use_jupiter_perps': True,  # Pull directly from Jupiter
            'primary_data_source': 'jupiter'
        })
        print("✅ Standalone mode enabled - works without bot infrastructure")
    
    def enable_integrated_mode(self):
        """Enable integrated mode (works with bot)"""
        self.update({
            'standalone_mode': False,
            'integrate_with_bot': True,
            'use_bot_data': True,
            'use_jupiter_perps': True,
            'primary_data_source': 'jupiter'
        })
        print("✅ Integrated mode enabled - works with bot")
    
    def enable_autonomous_bot(self):
        """Enable autonomous trading bot"""
        if not self.get('autonomous_bot_enabled'):
            print("⚠️ WARNING: Enabling autonomous bot - bot may execute trades automatically!")
            response = input("Are you sure? (yes/no): ").strip().lower()
            if response == 'yes':
                self.set('autonomous_bot_enabled', True)
                print("✅ Autonomous bot enabled")
            else:
                print("❌ Autonomous bot NOT enabled")
        else:
            print("✅ Autonomous bot already enabled")
    
    def disable_autonomous_bot(self):
        """Disable autonomous trading bot"""
        self.set('autonomous_bot_enabled', False)
        self.set('bot_auto_trade', False)
        print("✅ Autonomous bot disabled - manual trading only")
    
    def print_config(self):
        """Print current configuration"""
        print("\n" + "=" * 60)
        print("🤖 AI ASSISTANT CONFIGURATION")
        print("=" * 60)
        
        print(f"\n📊 MODE:")
        print(f"   Standalone Mode: {'✅ Enabled' if self.get('standalone_mode') else '❌ Disabled'}")
        print(f"   Integrated with Bot: {'✅ Yes' if self.get('integrate_with_bot') else '❌ No'}")
        print(f"   Autonomous Bot: {'⚠️ Enabled' if self.get('autonomous_bot_enabled') else '✅ Disabled'}")
        print(f"   Bot Auto-Trade: {'⚠️ Enabled' if self.get('bot_auto_trade') else '✅ Disabled'}")
        
        print(f"\n🤖 AI ASSISTANT:")
        print(f"   Enabled: {'✅ Yes' if self.get('ai_assistant_enabled') else '❌ No'}")
        print(f"   Auto-Refresh: {'✅ Yes' if self.get('ai_auto_refresh') else '❌ No'}")
        if self.get('ai_auto_refresh'):
            print(f"   Refresh Interval: {self.get('ai_refresh_interval')} seconds")
        
        print(f"\n📡 DATA SOURCES:")
        print(f"   Primary Source: {self.get('primary_data_source').upper()}")
        print(f"   Jupiter Perps: {'✅ Enabled' if self.get('use_jupiter_perps') else '❌ Disabled'}")
        print(f"   Use Bot Data: {'✅ Yes' if self.get('use_bot_data') else '❌ No'}")
        
        print(f"\n🔧 OLLAMA:")
        ollama_url = self.get('ollama_url') or 'Auto-detect from env'
        print(f"   URL: {ollama_url}")
        print(f"   Model: {self.get('ollama_model')}")
        
        print(f"\n📊 DISPLAY:")
        print(f"   Detailed Analysis: {'✅ Yes' if self.get('show_detailed_analysis') else '❌ No'}")
        print(f"   High Confidence Alerts: {'✅ Yes' if self.get('alert_on_high_confidence') else '❌ No'}")
        print(f"   Confidence Threshold: {self.get('high_confidence_threshold')}/10")
        
        print(f"\n📈 COMET ML:")
        print(f"   Enabled: {'✅ Yes' if self.get('comet_enabled') else '❌ No'}")
        
        print("=" * 60 + "\n")
    
    def interactive_setup(self):
        """Interactive configuration setup"""
        print("\n🤖 AI Assistant Configuration Setup")
        print("=" * 60)
        
        # Mode selection
        print("\n1️⃣ Select Mode:")
        print("   1. Standalone (works without bot - for manual trading)")
        print("   2. Integrated (works with bot - shows recommendations in cycles)")
        print("   3. Keep current settings")
        
        choice = input("\nSelect [1-3]: ").strip()
        
        if choice == "1":
            self.enable_standalone_mode()
        elif choice == "2":
            self.enable_integrated_mode()
        
        # AI Assistant settings
        if self.get('ai_assistant_enabled'):
            auto_refresh = input("\n2️⃣ Enable AI auto-refresh? (y/N): ").strip().lower()
            if auto_refresh == 'y':
                interval = input("   Refresh interval (seconds) [60]: ").strip()
                try:
                    interval = int(interval) if interval else 60
                    self.set('ai_auto_refresh', True)
                    self.set('ai_refresh_interval', interval)
                    print(f"✅ Auto-refresh enabled ({interval}s interval)")
                except ValueError:
                    print("❌ Invalid interval, using default")
        
        # Autonomous bot (if integrated)
        if not self.get('standalone_mode'):
            enable_bot = input("\n3️⃣ Enable autonomous trading bot? (y/N): ").strip().lower()
            if enable_bot == 'y':
                self.enable_autonomous_bot()
        
        # Save configuration
        self._save_config()
        print("\n✅ Configuration saved!")
        self.print_config()


# Global config instance
_config_instance: Optional[AIAssistantConfig] = None

def get_config() -> AIAssistantConfig:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = AIAssistantConfig()
    return _config_instance

def reload_config():
    """Reload configuration from file"""
    global _config_instance
    _config_instance = AIAssistantConfig()
    return _config_instance

# Convenience functions
def is_standalone_mode() -> bool:
    """Check if in standalone mode"""
    return get_config().get('standalone_mode', True)

def is_autonomous_bot_enabled() -> bool:
    """Check if autonomous bot is enabled"""
    return get_config().get('autonomous_bot_enabled', False)

def is_ai_assistant_enabled() -> bool:
    """Check if AI assistant is enabled"""
    return get_config().get('ai_assistant_enabled', True)


if __name__ == "__main__":
    # Interactive configuration setup
    config = get_config()
    config.interactive_setup()

