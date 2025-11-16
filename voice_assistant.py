#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice-Enabled Trading AI Assistant
Uses Ollama with voice capabilities for hands-free trading recommendations
Works standalone - no dependencies on bot infrastructure
"""
import os
import json
import time
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from threading import Thread, Event

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# Voice recognition libraries
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("WARNING: Voice libraries not installed. Install with: pip install SpeechRecognition pyttsx3")

# Import AI assistant components
from seamless_trading_assistant import SeamlessTradingAssistant
from ai_assistant_config import get_config


class VoiceTradingAssistant:
    """
    Voice-enabled trading assistant
    Speak commands, hear recommendations - hands-free operation
    """
    
    def __init__(self, 
                 use_ollama_tts: bool = False,
                 voice_enabled: bool = True):
        """
        Initialize voice-enabled assistant
        
        Args:
            use_ollama_tts: Use Ollama for text-to-speech (if supported)
            voice_enabled: Enable voice input/output
        """
        self.config = get_config()
        self.use_ollama_tts = use_ollama_tts
        self.voice_enabled = voice_enabled and VOICE_AVAILABLE
        
        # Initialize AI assistant
        self.assistant = SeamlessTradingAssistant()
        
        # Initialize voice components
        self.recognizer = None
        self.tts_engine = None
        self.is_listening = False
        self.stop_listening = Event()
        
        if self.voice_enabled:
            try:
                # Speech recognition
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                
                # Text-to-speech (local)
                if not use_ollama_tts:
                    self.tts_engine = pyttsx3.init()
                    # Configure voice settings
                    voices = self.tts_engine.getProperty('voices')
                    if voices:
                        # Prefer female voice if available (often clearer)
                        for voice in voices:
                            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                                self.tts_engine.setProperty('voice', voice.id)
                                break
                        else:
                            self.tts_engine.setProperty('voice', voices[0].id)
                    
                    self.tts_engine.setProperty('rate', 150)  # Speech rate
                    self.tts_engine.setProperty('volume', 0.9)  # Volume
                
                print("OK - Voice capabilities enabled")
            except Exception as e:
                print(f"WARNING: Voice initialization error: {e}")
                self.voice_enabled = False
    
    def speak(self, text: str, wait: bool = True):
        """Speak text aloud"""
        if not self.voice_enabled:
            print(f"[SPEAK] {text}")
            return
        
        try:
            if self.use_ollama_tts:
                # Use Ollama TTS if available (future feature)
                print(f"[SPEAK] {text}")
                # TODO: Implement Ollama TTS integration when available
            else:
                # Use local TTS
                print(f"[SPEAK] Speaking: {text[:100]}...")
                self.tts_engine.say(text)
                if wait:
                    self.tts_engine.runAndWait()
        except Exception as e:
            print(f"WARNING: TTS error: {e}")
            print(f"[SPEAK] {text}")
    
    def listen(self, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> Optional[str]:
        """Listen for voice command"""
        if not self.voice_enabled:
            return None
        
        try:
            with sr.Microphone() as source:
                print("[LISTEN] Listening... (speak now)")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("[PROCESS] Processing audio...")
                
                # Recognize speech using Google's service (free, requires internet)
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"OK - Heard: {text}")
                    return text.lower()
                except sr.UnknownValueError:
                    print("WARNING: Could not understand audio")
                    return None
                except sr.RequestError as e:
                    print(f"WARNING: Speech recognition error: {e}")
                    return None
                    
        except Exception as e:
            print(f"WARNING: Listening error: {e}")
            return None
    
    def get_voice_command(self) -> Optional[str]:
        """Get voice command with prompts"""
        if not self.voice_enabled:
            return None
        
        self.speak("Ready for command. Say analyze, quick recommendation, or status")
        command = self.listen(timeout=5.0)
        return command
    
    def analyze_with_voice(self) -> Dict[str, Any]:
        """Get AI analysis and speak recommendation"""
        print("\n[ANALYZE] Getting AI recommendation...")
        self.speak("Analyzing market data. This may take a few seconds.", wait=False)
        
        # Get analysis
        result = self.assistant.analyze_and_recommend(show_details=False)
        
        # Extract recommendation
        rec = result['recommendation']
        action = rec['action']
        confidence = rec['confidence']
        market_data = result['complete_data']['market_data']
        price = market_data.get('price', 0)
        
        # Format voice response
        response = (
            f"AI Recommendation: {action}. "
            f"Confidence level {confidence} out of 10. "
            f"Current ETH price on Jupiter is ${price:,.2f}. "
        )
        
        # Add Jupiter insights if available
        if 'jupiter_insights' in result:
            jup = result['jupiter_insights']
            sentiment = jup.get('sentiment', 'neutral')
            if sentiment != 'neutral':
                response += f"Jupiter sentiment is {sentiment}. "
        
        # Add reasoning snippet
        analysis = result.get('analysis', '')
        if analysis:
            brief_reason = analysis[:150].replace('\n', ' ')
            response += f"Analysis: {brief_reason}."
        
        # Speak recommendation
        self.speak(response)
        
        # Also display on screen
        print("\n" + "=" * 70)
        print(f"AI RECOMMENDATION: {action}")
        print(f"   Confidence: {confidence}/10")
        print(f"   Jupiter Price: ${price:,.2f}")
        print("=" * 70)
        
        return result
    
    def quick_recommendation_voice(self):
        """Get quick recommendation and speak it"""
        print("\n[QUICK] Getting quick recommendation...")
        self.speak("Getting quick recommendation")
        
        # Gather minimal data
        data = self.assistant.gather_all_data()
        market_data = data['market_data']
        price = market_data.get('price', 3500)
        
        # Get quick recommendation
        quick_rec = self.assistant.assistant.get_quick_recommendation(
            price=price,
            indicators={
                'rsi': market_data.get('rsi', 50),
                'ema_trend': 'bullish' if market_data.get('price', 0) > market_data.get('ema_12', 0) else 'bearish',
                'volume': 'high' if market_data.get('volume_24h', 0) > 1000000 else 'low'
            }
        )
        
        # Speak recommendation
        voice_text = f"Quick recommendation: {quick_rec}"
        self.speak(voice_text)
        
        print(f"\n[QUICK] {quick_rec}")
        
        return quick_rec
    
    def status_voice(self):
        """Speak current status"""
        data = self.assistant.gather_all_data()
        market_data = data['market_data']
        price = market_data.get('price', 0)
        
        # Get Jupiter insights if available
        if 'jupiter_insights' in data:
            jup = data['jupiter_insights']
            volume = jup.get('volume_24h', 0)
            sentiment = jup.get('sentiment', 'neutral')
            
            status = (
                f"Current ETH price on Jupiter is ${price:,.2f}. "
                f"24 hour volume is ${volume:,.0f}. "
                f"Jupiter sentiment is {sentiment}."
            )
        else:
            status = f"Current ETH price is ${price:,.2f}."
        
        self.speak(status)
        print(f"\n[STATUS] {status}")
    
    def continuous_voice_mode(self, interval: int = 60):
        """Continuous voice mode - periodically speaks recommendations"""
        print(f"\n[CONTINUOUS] Continuous Voice Mode (every {interval} seconds)")
        print("Say 'stop' to exit")
        self.speak(f"Starting continuous voice mode. Updates every {interval} seconds")
        
        self.is_listening = True
        last_update = time.time()
        
        try:
            while self.is_listening and not self.stop_listening.is_set():
                # Check for voice command to stop
                try:
                    command = self.listen(timeout=1.0, phrase_time_limit=3.0)
                    if command and 'stop' in command:
                        self.speak("Stopping continuous mode")
                        break
                except:
                    pass  # No command received, continue
                
                # Periodic analysis
                current_time = time.time()
                if current_time - last_update >= interval:
                    self.analyze_with_voice()
                    last_update = current_time
                    self.speak(f"Next update in {interval} seconds")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.speak("Stopping continuous mode")
        finally:
            self.is_listening = False
    
    def interactive_voice_mode(self):
        """Interactive voice mode - respond to voice commands"""
        print("\n[INTERACTIVE] Interactive Voice Mode")
        print("Commands: 'analyze', 'quick', 'status', 'help', 'exit'")
        self.speak("Interactive voice mode activated")
        
        while True:
            try:
                command = self.get_voice_command()
                
                if not command:
                    continue
                
                # Process commands
                if any(word in command for word in ['analyze', 'analysis', 'recommendation', 'full']):
                    self.analyze_with_voice()
                    
                elif any(word in command for word in ['quick', 'fast', 'brief']):
                    self.quick_recommendation_voice()
                    
                elif any(word in command for word in ['status', 'price', 'current']):
                    self.status_voice()
                    
                elif any(word in command for word in ['help', 'commands']):
                    help_text = (
                        "Commands: Say 'analyze' for full recommendation, "
                        "'quick' for brief recommendation, "
                        "'status' for current price and sentiment, "
                        "or 'exit' to quit"
                    )
                    self.speak(help_text)
                    
                elif any(word in command for word in ['exit', 'quit', 'stop']):
                    self.speak("Exiting voice mode. Goodbye")
                    break
                    
                else:
                    self.speak(f"Command not recognized: {command}. Say help for available commands")
                    
            except KeyboardInterrupt:
                self.speak("Exiting voice mode")
                break
            except Exception as e:
                print(f"WARNING: Error: {e}")
                self.speak("Sorry, an error occurred")


def main():
    """Main voice assistant"""
    print("Voice-Enabled Trading AI Assistant")
    print("=" * 70)
    
    if not VOICE_AVAILABLE:
        print("\nERROR: Voice libraries not available!")
        print("Install with: pip install SpeechRecognition pyttsx3")
        print("\nYou can also use text-only mode:")
        from seamless_trading_assistant import main as text_main
        text_main()
        return
    
    # Check Ollama connection
    print("\n[TEST] Testing Ollama connection...")
    assistant = VoiceTradingAssistant()
    
    if not assistant.assistant.assistant.ollama.test_connection():
        print("ERROR: Cannot connect to Ollama!")
        print("Check your OLLAMA_URL environment variable")
        print("Or set in .env file: OLLAMA_URL=your-url")
        return
    
    print("OK - Ollama connected!")
    
    # Main menu
    while True:
        print("\n" + "=" * 70)
        print("VOICE TRADING ASSISTANT")
        print("=" * 70)
        print("1. Interactive voice mode (respond to commands)")
        print("2. Continuous voice mode (periodic updates)")
        print("3. Single analysis (voice)")
        print("4. Quick recommendation (voice)")
        print("5. Current status (voice)")
        print("6. Text-only mode (no voice)")
        print("7. Exit")
        
        choice = input("\nSelect option [1-7]: ").strip()
        
        if choice == "1":
            assistant.interactive_voice_mode()
            
        elif choice == "2":
            interval = input("Update interval (seconds) [60]: ").strip()
            try:
                interval = int(interval) if interval else 60
                assistant.continuous_voice_mode(interval)
            except ValueError:
                print("ERROR: Invalid interval")
                
        elif choice == "3":
            assistant.analyze_with_voice()
            
        elif choice == "4":
            assistant.quick_recommendation_voice()
            
        elif choice == "5":
            assistant.status_voice()
            
        elif choice == "6":
            from seamless_trading_assistant import main as text_main
            text_main()
            
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("ERROR: Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

