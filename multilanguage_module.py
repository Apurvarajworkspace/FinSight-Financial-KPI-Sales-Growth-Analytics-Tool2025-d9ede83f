"""
Multi-Language Support Module
Internationalization (i18n) and localization (l10n) support
"""

import json
from datetime import datetime


class LanguageManager:
    """Manage language configuration and switching"""
    
    def __init__(self, default_language='en'):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
        self.current_language = default_language
        self.language_preferences = {}
    
    def set_language(self, language_code):
        """Set current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            return {'status': 'set', 'language': self.supported_languages[language_code]}
        return {'status': 'error', 'message': 'Language not supported'}
    
    def get_current_language(self):
        """Get current language"""
        return {
            'language_code': self.current_language,
            'language_name': self.supported_languages[self.current_language]
        }
    
    def get_supported_languages(self):
        """Get all supported languages"""
        return {
            'count': len(self.supported_languages),
            'languages': self.supported_languages
        }
    
    def set_user_preference(self, user_id, language_code):
        """Set user language preference"""
        if language_code not in self.supported_languages:
            return None
        
        self.language_preferences[user_id] = {
            'language': language_code,
            'set_at': datetime.now().isoformat()
        }
        return {'user_id': user_id, 'language': language_code}


class TranslationManager:
    """Manage text translations"""
    
    def __init__(self):
        self.translations = self._load_default_translations()
        self.custom_translations = {}
        self.translation_stats = {}
    
    def _load_default_translations(self):
        """Load default translations"""
        return {
            'en': {'greeting': 'Hello', 'welcome': 'Welcome', 'logout': 'Logout'},
            'es': {'greeting': 'Hola', 'welcome': 'Bienvenido', 'logout': 'Cerrar'},
            'fr': {'greeting': 'Bonjour', 'welcome': 'Bienvenue', 'logout': 'Deconnexion'},
            'de': {'greeting': 'Hallo', 'welcome': 'Willkommen', 'logout': 'Abmelden'},
            'zh': {'greeting': 'Nihao', 'welcome': 'Huanying', 'logout': 'Tuichu'},
            'ja': {'greeting': 'Konnichiwa', 'welcome': 'Yokoso', 'logout': 'Logout'},
            'pt': {'greeting': 'Ola', 'welcome': 'Bemvindo', 'logout': 'Sair'},
            'ru': {'greeting': 'Zdravstvuyte', 'welcome': 'Dobro', 'logout': 'Vykhod'},
            'ar': {'greeting': 'Assalam', 'welcome': 'Ahlan', 'logout': 'Khoruj'},
            'hi': {'greeting': 'Namaste', 'welcome': 'Swagat', 'logout': 'Logout'}
        }
    
    def translate(self, text_key, language_code='en'):
        """Translate text key"""
        if language_code in self.translations and text_key in self.translations[language_code]:
            return self.translations[language_code][text_key]
        return text_key
    
    def add_translation(self, language_code, key, translation):
        """Add custom translation"""
        if language_code not in self.translations:
            self.translations[language_code] = {}
        self.translations[language_code][key] = translation
        return {'status': 'added'}


class LocalizationManager:
    """Manage localization"""
    
    def __init__(self):
        self.locale_settings = {
            'en': {'currency': 'USD', 'date_format': 'MM/DD/YYYY'},
            'es': {'currency': 'EUR', 'date_format': 'DD/MM/YYYY'},
            'fr': {'currency': 'EUR', 'date_format': 'DD/MM/YYYY'},
            'de': {'currency': 'EUR', 'date_format': 'DD.MM.YYYY'},
            'zh': {'currency': 'CNY', 'date_format': 'YYYY-MM-DD'},
            'ja': {'currency': 'JPY', 'date_format': 'YYYY/MM/DD'},
            'pt': {'currency': 'BRL', 'date_format': 'DD/MM/YYYY'},
            'ru': {'currency': 'RUB', 'date_format': 'DD.MM.YYYY'},
            'ar': {'currency': 'SAR', 'date_format': 'DD/MM/YYYY'},
            'hi': {'currency': 'INR', 'date_format': 'DD/MM/YYYY'}
        }
    
    def format_currency(self, amount, language_code='en'):
        """Format currency"""
        if language_code not in self.locale_settings:
            language_code = 'en'
        currency = self.locale_settings[language_code]['currency']
        return f"{currency} {amount:,.2f}"
    
    def get_locale_settings(self, language_code='en'):
        """Get locale settings"""
        return self.locale_settings.get(language_code, self.locale_settings['en'])


class ContentLocalization:
    """Localize content"""
    
    def __init__(self):
        self.localized_content = {}
        self.language_manager = LanguageManager()
        self.translation_manager = TranslationManager()
        self.localization_manager = LocalizationManager()
    
    def localize_content(self, content_id, language_code='en'):
        """Localize content"""
        self.localized_content[content_id] = {
            'content_id': content_id,
            'language': language_code,
            'localized_at': datetime.now().isoformat()
        }
        return self.localized_content[content_id]
    
    def get_localized_content(self, content_id):
        """Get localized content"""
        return self.localized_content.get(content_id)


def run_multilanguage_demo():
    """Demo function for multi-language support"""
    print("\n" + "="*70)
    print("MULTI-LANGUAGE SUPPORT DEMO")
    print("="*70)
    
    lang_mgr = LanguageManager()
    trans_mgr = TranslationManager()
    locale_mgr = LocalizationManager()
    content_loc = ContentLocalization()
    
    # 1. Language support
    print("\n[1] Language Support...")
    print("-" * 70)
    langs = lang_mgr.get_supported_languages()
    print(f"[DONE] Supported Languages: {langs['count']}")
    
    # 2. Language switching
    print("\n[2] Language Switching...")
    print("-" * 70)
    lang_mgr.set_language('es')
    current = lang_mgr.get_current_language()
    print(f"[DONE] Language Set: {current['language_name']}")
    
    # 3. Translations
    print("\n[3] Text Translations...")
    print("-" * 70)
    for code in ['en', 'es', 'fr', 'de', 'ja']:
        greeting = trans_mgr.translate('greeting', code)
        print(f"[DONE] Greeting ({code}): {greeting}")
    
    # 4. Localization
    print("\n[4] Localization Formatting...")
    print("-" * 70)
    for code in ['en', 'es', 'fr', 'de', 'ja']:
        currency = locale_mgr.format_currency(1000000, code)
        print(f"[DONE] Format ({code}): {currency}")
    
    # 5. User preferences
    print("\n[5] User Preferences...")
    print("-" * 70)
    lang_mgr.set_user_preference('USER001', 'fr')
    lang_mgr.set_user_preference('USER002', 'es')
    print("[DONE] User Preferences: 2 saved")
    
    print("\n" + "="*70)
    print("[DONE] MULTI-LANGUAGE SUPPORT DEMO COMPLETED")
    print("="*70)
