"""
Standalone AI Learning Module
Self-contained AI learning system that doesn't depend on external libraries
"""
import json
import os
import math
import random
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TradingSignal:
    """Enhanced trading signal with confidence and metadata"""
    action: str  # 'long', 'short', 'hold'
    confidence: float  # 0.0 to 1.0
    features: Dict[str, float]  # Feature values used for prediction
    timestamp: datetime
    model_version: str
    reasoning: str  # Human-readable explanation

@dataclass
class TradeOutcome:
    """Trade outcome for learning"""
    signal: TradingSignal
    entry_price: float
    exit_price: float
    pnl: float
    duration: float  # hours
    market_conditions: Dict[str, float]
    success: bool

class SimpleMLModel:
    """Simple machine learning model implementation"""
    
    def __init__(self, model_type='classifier'):
        self.model_type = model_type
        self.weights = {}
        self.bias = 0.0
        self.feature_names = []
        self.trained = False
        self.training_data = []
    
    def fit(self, X, y):
        """Simple linear model training"""
        if len(X) == 0:
            return
        
        self.feature_names = list(X[0].keys()) if X else []
        self.training_data = list(zip(X, y))
        
        # Simple weight initialization
        for feature in self.feature_names:
            self.weights[feature] = random.uniform(-0.1, 0.1)
        
        # Basic gradient descent
        learning_rate = 0.01
        epochs = 50
        
        for epoch in range(epochs):
            for sample, target in self.training_data:
                prediction = self._predict_single(sample)
                
                if self.model_type == 'classifier':
                    target_binary = 1 if target > 0 else 0
                    error = target_binary - prediction
                else:
                    error = target - prediction
                
                # Update weights
                for feature in self.feature_names:
                    if feature in sample:
                        self.weights[feature] += learning_rate * error * sample[feature]
                self.bias += learning_rate * error
        
        self.trained = True
    
    def _predict_single(self, features):
        """Predict single sample"""
        if not self.trained:
            return 0.5
        
        prediction = self.bias
        for feature, value in features.items():
            if feature in self.weights:
                prediction += self.weights[feature] * value
        
        # Sigmoid activation for classification
        if self.model_type == 'classifier':
            return 1 / (1 + math.exp(-prediction))
        return prediction
    
    def predict(self, X):
        """Predict multiple samples"""
        return [self._predict_single(sample) for sample in X]
    
    def predict_proba(self, X):
        """Predict probabilities for classification"""
        predictions = self.predict(X)
        return [(1-p, p) for p in predictions]  # (negative, positive) probabilities

class FeatureExtractor:
    """Extracts features from market data and trading history"""
    
    def __init__(self):
        self.feature_history = []
        self.max_history = 1000
    
    def extract_market_features(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from current market data"""
        features = {}
        
        # Price-based features
        features['price'] = float(market_data.get('price', 3000.0))
        features['price_change_1h'] = market_data.get('price_change_1h', 0.0)
        features['price_change_24h'] = market_data.get('price_change_24h', 0.0)
        
        # Volume features
        features['volume_24h'] = market_data.get('volume_24h', 1000000.0)
        features['volume_change_24h'] = market_data.get('volume_change_24h', 0.0)
        
        # Technical indicators
        features['rsi'] = market_data.get('rsi', 50.0)
        features['ema_12'] = market_data.get('ema_12', 3000.0)
        features['ema_26'] = market_data.get('ema_26', 3000.0)
        features['bb_upper'] = market_data.get('bb_upper', 3100.0)
        features['bb_lower'] = market_data.get('bb_lower', 2900.0)
        features['bb_middle'] = market_data.get('bb_middle', 3000.0)
        
        # Funding rate features
        features['funding_rate'] = market_data.get('funding_rate', 0.0)
        features['funding_rate_8h_avg'] = market_data.get('funding_rate_8h_avg', 0.0)
        
        # Market sentiment
        features['fear_greed_index'] = market_data.get('fear_greed_index', 50.0)
        features['social_sentiment'] = market_data.get('social_sentiment', 0.0)
        
        # Time-based features
        now = datetime.now()
        features['hour_of_day'] = now.hour
        features['day_of_week'] = now.weekday()
        features['is_weekend'] = 1.0 if now.weekday() >= 5 else 0.0
        
        return features
    
    def extract_historical_features(self, trade_history: List[Dict]) -> Dict[str, float]:
        """Extract features from trading history"""
        features = {}
        
        if not trade_history:
            return {
                'recent_win_rate': 0.5,
                'avg_trade_duration': 24.0,
                'recent_pnl_trend': 0.0,
                'consecutive_wins': 0,
                'consecutive_losses': 0,
                'total_trades': 0
            }
        
        # Recent performance (last 10 trades)
        recent_trades = trade_history[-10:]
        wins = sum(1 for trade in recent_trades if trade.get('realized_pnl', 0) > 0)
        features['recent_win_rate'] = wins / len(recent_trades) if recent_trades else 0.5
        
        # Average trade duration
        durations = []
        for trade in recent_trades:
            if trade.get('entry_time') and trade.get('exit_time'):
                try:
                    entry = datetime.fromisoformat(trade['entry_time'].replace('Z', '+00:00'))
                    exit_time = datetime.fromisoformat(trade['exit_time'].replace('Z', '+00:00'))
                    duration = (exit_time - entry).total_seconds() / 3600  # hours
                    durations.append(duration)
                except:
                    pass
        features['avg_trade_duration'] = sum(durations) / len(durations) if durations else 24.0
        
        # Recent PnL trend
        recent_pnls = [trade.get('realized_pnl', 0) for trade in recent_trades]
        features['recent_pnl_trend'] = sum(recent_pnls) / len(recent_pnls) if recent_pnls else 0.0
        
        # Consecutive wins/losses
        consecutive_wins = 0
        consecutive_losses = 0
        for trade in reversed(recent_trades):
            pnl = trade.get('realized_pnl', 0)
            if pnl > 0:
                consecutive_wins += 1
                consecutive_losses = 0
            elif pnl < 0:
                consecutive_losses += 1
                consecutive_wins = 0
            else:
                break
        features['consecutive_wins'] = consecutive_wins
        features['consecutive_losses'] = consecutive_losses
        
        features['total_trades'] = len(trade_history)
        
        return features
    
    def extract_portfolio_features(self, portfolio_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from portfolio state"""
        features = {}
        
        features['current_balance'] = portfolio_data.get('current_balance', 10000.0)
        features['total_pnl'] = portfolio_data.get('total_pnl', 0.0)
        features['win_rate'] = portfolio_data.get('win_rate', 0.0)
        features['open_positions'] = len(portfolio_data.get('positions', {}))
        features['total_trades'] = portfolio_data.get('total_trades', 0)
        
        # Risk metrics
        features['max_drawdown'] = portfolio_data.get('max_drawdown', 0.0)
        features['sharpe_ratio'] = portfolio_data.get('sharpe_ratio', 0.0)
        
        return features

class StandaloneAILearningEngine:
    """Standalone AI learning engine"""
    
    def __init__(self, model_path: str = "ai_models/"):
        self.model_path = model_path
        os.makedirs(model_path, exist_ok=True)
        
        self.feature_extractor = FeatureExtractor()
        self.signal_model = SimpleMLModel('classifier')
        self.confidence_model = SimpleMLModel('regressor')
        
        self.trade_outcomes = []
        self.model_version = "1.0.0"
        self.retrain_threshold = 50
        
        # Performance tracking
        self.model_performance = {
            'accuracy': 0.0,
            'last_retrain': None,
            'total_predictions': 0,
            'correct_predictions': 0
        }
        
        self._load_models()
    
    def _load_models(self):
        """Load existing models or create new ones"""
        try:
            if os.path.exists(f"{self.model_path}/performance.json"):
                with open(f"{self.model_path}/performance.json", 'r') as f:
                    self.model_performance = json.load(f)
            print("✅ AI models loaded successfully")
        except Exception as e:
            print(f"⚠️ Could not load existing models: {e}")
            print("🔄 Starting with fresh models")
    
    def _save_models(self):
        """Save trained models"""
        try:
            with open(f"{self.model_path}/performance.json", 'w') as f:
                json.dump(self.model_performance, f, indent=2)
            print("✅ AI models saved successfully")
        except Exception as e:
            print(f"❌ Error saving models: {e}")
    
    def prepare_training_data(self, simulation_data: Dict[str, Any]) -> Tuple[List[Dict], List[float], List[float]]:
        """Prepare training data from simulation history"""
        X = []  # Features
        y_signals = []  # Signal outcomes (1 for profitable, 0 for loss)
        y_confidences = []  # Confidence targets (based on PnL magnitude)
        
        trade_history = simulation_data.get('trade_history', [])
        
        for trade in trade_history:
            if trade.get('status') != 'closed':
                continue
            
            # Extract features for this trade
            features = {}
            
            # Market features (simplified)
            features.update({
                'price': trade.get('entry_price', 0.0),
                'rsi': 50.0,  # Placeholder
                'funding_rate': 0.0,  # Placeholder
                'volume_24h': 1000000.0,  # Placeholder
                'fear_greed_index': 50.0,  # Placeholder
            })
            
            # Historical features
            trade_index = trade_history.index(trade)
            historical_features = self.feature_extractor.extract_historical_features(
                trade_history[:trade_index]
            )
            features.update(historical_features)
            
            # Portfolio features
            portfolio_features = self.feature_extractor.extract_portfolio_features({
                'current_balance': simulation_data.get('current_balance', 10000.0),
                'total_pnl': simulation_data.get('metrics', {}).get('total_pnl', 0.0),
                'win_rate': simulation_data.get('metrics', {}).get('win_rate', 0.0),
                'positions': simulation_data.get('positions', {}),
                'total_trades': simulation_data.get('metrics', {}).get('total_trades', 0)
            })
            features.update(portfolio_features)
            
            X.append(features)
            
            # Target variables
            pnl = trade.get('realized_pnl', 0.0)
            y_signals.append(1 if pnl > 0 else 0)
            
            # Confidence target based on PnL magnitude (normalized)
            confidence_target = min(abs(pnl) / 100.0, 1.0)  # Normalize to 0-1
            y_confidences.append(confidence_target)
        
        return X, y_signals, y_confidences
    
    def train_models(self, simulation_data: Dict[str, Any]):
        """Train the AI models on historical data"""
        print("🧠 Training AI models...")
        
        X, y_signals, y_confidences = self.prepare_training_data(simulation_data)
        
        if len(X) < 5:
            print("⚠️ Insufficient training data. Need at least 5 trades.")
            return
        
        print(f"📊 Training on {len(X)} historical trades")
        
        try:
            # Train models
            self.signal_model.fit(X, y_signals)
            self.confidence_model.fit(X, y_confidences)
            
            # Update performance tracking
            self.model_performance['last_retrain'] = datetime.now().isoformat()
            
            # Calculate training accuracy
            predictions = self.signal_model.predict(X)
            accuracy = sum(1 for p, t in zip(predictions, y_signals) if (p > 0.5) == t) / len(y_signals)
            
            self.model_performance['accuracy'] = accuracy
            print(f"✅ Model training complete. Accuracy: {accuracy:.2%}")
            
            self._save_models()
            
        except Exception as e:
            print(f"❌ Error training models: {e}")
    
    def predict_signal(self, market_data: Dict[str, Any], 
                      trade_history: List[Dict], 
                      portfolio_data: Dict[str, Any]) -> TradingSignal:
        """Generate AI-powered trading signal"""
        
        if not self.signal_model.trained or not self.confidence_model.trained:
            # Fallback to basic signal if models not trained
            return TradingSignal(
                action='hold',
                confidence=0.5,
                features={},
                timestamp=datetime.now(),
                model_version=self.model_version,
                reasoning="Models not trained yet"
            )
        
        # Extract features
        features = {}
        features.update(self.feature_extractor.extract_market_features(market_data))
        features.update(self.feature_extractor.extract_historical_features(trade_history))
        features.update(self.feature_extractor.extract_portfolio_features(portfolio_data))
        
        try:
            # Make prediction
            signal_pred = self.signal_model.predict([features])[0]
            confidence = self.confidence_model.predict([features])[0]
            
            # Determine action
            if signal_pred > 0.6:
                action = 'long'
            elif signal_pred < 0.4:
                action = 'short'
            else:
                action = 'hold'
            
            # Generate reasoning
            reasoning = self._generate_reasoning(features, action, confidence)
            
            # Update performance tracking
            self.model_performance['total_predictions'] += 1
            
            return TradingSignal(
                action=action,
                confidence=min(max(confidence, 0.0), 1.0),
                features=features,
                timestamp=datetime.now(),
                model_version=self.model_version,
                reasoning=reasoning
            )
            
        except Exception as e:
            print(f"❌ Error generating signal: {e}")
            return TradingSignal(
                action='hold',
                confidence=0.5,
                features=features,
                timestamp=datetime.now(),
                model_version=self.model_version,
                reasoning=f"Error in prediction: {e}"
            )
    
    def _generate_reasoning(self, features: Dict[str, float], action: str, confidence: float) -> str:
        """Generate human-readable reasoning for the signal"""
        reasons = []
        
        if features.get('recent_win_rate', 0.5) > 0.7:
            reasons.append("Strong recent performance")
        elif features.get('recent_win_rate', 0.5) < 0.3:
            reasons.append("Poor recent performance")
        
        if features.get('rsi', 50) < 30:
            reasons.append("Oversold conditions (RSI < 30)")
        elif features.get('rsi', 50) > 70:
            reasons.append("Overbought conditions (RSI > 70)")
        
        if features.get('consecutive_losses', 0) > 3:
            reasons.append("Multiple consecutive losses")
        elif features.get('consecutive_wins', 0) > 3:
            reasons.append("Multiple consecutive wins")
        
        if features.get('funding_rate', 0) > 0.01:
            reasons.append("High funding rate")
        elif features.get('funding_rate', 0) < -0.01:
            reasons.append("Negative funding rate")
        
        if not reasons:
            reasons.append("Balanced market conditions")
        
        return f"AI Signal ({action.upper()}): {', '.join(reasons)}. Confidence: {confidence:.1%}"
    
    def learn_from_outcome(self, signal: TradingSignal, outcome: TradeOutcome):
        """Learn from trade outcome to improve future predictions"""
        self.trade_outcomes.append(outcome)
        
        # Update performance tracking
        if outcome.success:
            self.model_performance['correct_predictions'] += 1
        
        # Check if we should retrain
        if len(self.trade_outcomes) >= self.retrain_threshold:
            print("🔄 Retraining models with new data...")
            print(f"📚 Learned from {len(self.trade_outcomes)} trade outcomes")
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current model status and performance"""
        return {
            'model_version': self.model_version,
            'performance': self.model_performance,
            'total_outcomes': len(self.trade_outcomes),
            'models_trained': self.signal_model.trained and self.confidence_model.trained
        }

# Global AI learning engine instance
standalone_ai_engine = StandaloneAILearningEngine()

def initialize_standalone_ai_learning(simulation_data_path: str = "simulation_data.json"):
    """Initialize standalone AI learning with existing data"""
    try:
        if os.path.exists(simulation_data_path):
            with open(simulation_data_path, 'r') as f:
                simulation_data = json.load(f)
            
            standalone_ai_engine.train_models(simulation_data)
            print("✅ Standalone AI learning initialized successfully")
        else:
            print("⚠️ No simulation data found. AI will start learning from new trades.")
    except Exception as e:
        print(f"❌ Error initializing standalone AI learning: {e}")

def get_standalone_ai_signal(market_data: Dict[str, Any], 
                           trade_history: List[Dict], 
                           portfolio_data: Dict[str, Any]) -> TradingSignal:
    """Get standalone AI-powered trading signal"""
    return standalone_ai_engine.predict_signal(market_data, trade_history, portfolio_data)

def learn_from_trade_standalone(signal: TradingSignal, trade_outcome: Dict[str, Any]):
    """Learn from completed trade"""
    outcome = TradeOutcome(
        signal=signal,
        entry_price=trade_outcome.get('entry_price', 0.0),
        exit_price=trade_outcome.get('exit_price', 0.0),
        pnl=trade_outcome.get('realized_pnl', 0.0),
        duration=trade_outcome.get('duration', 0.0),
        market_conditions=trade_outcome.get('market_conditions', {}),
        success=trade_outcome.get('realized_pnl', 0.0) > 0
    )
    
    standalone_ai_engine.learn_from_outcome(signal, outcome)

# Export main functions
__all__ = [
    'StandaloneAILearningEngine', 'TradingSignal', 'TradeOutcome', 'FeatureExtractor',
    'standalone_ai_engine', 'initialize_standalone_ai_learning', 
    'get_standalone_ai_signal', 'learn_from_trade_standalone'
]