/**
 * ChatWidget Translations
 * 
 * UI strings for the AI Tutor chat widget in all supported languages.
 * Add new languages by adding a new key to the translations object.
 */

export type Locale = 'en' | 'fr' | 'ar' | 'ur';

export interface ChatWidgetStrings {
  title: string;
  placeholder: string;
  send: string;
  typing: string;
  selectedText: string;
  sources: string;
  error: string;
  close: string;
  clear: string;
  emptyStateGreeting: string;
  emptyStateHint: string;
  selectedTextHint: string;
  aiResponseNote: string;
}

export const translations: Record<Locale, ChatWidgetStrings> = {
  // English (default)
  en: {
    title: 'AI Tutor',
    placeholder: 'Ask a question about the textbook...',
    send: 'Send',
    typing: 'AI is thinking...',
    selectedText: 'Selected:',
    sources: 'Sources:',
    error: 'Sorry, I encountered an error. Please try again.',
    close: 'Close chat',
    clear: 'Clear chat',
    emptyStateGreeting: '👋 Hi! I\'m your AI tutor.',
    emptyStateHint: 'Ask me anything about the textbook content!',
    selectedTextHint: '💡 I can see you\'ve selected some text. Ask me about it!',
    aiResponseNote: 'AI responds in English',
  },

  // French (Français)
  fr: {
    title: 'Tuteur IA',
    placeholder: 'Posez une question sur le manuel...',
    send: 'Envoyer',
    typing: 'L\'IA réfléchit...',
    selectedText: 'Sélectionné :',
    sources: 'Sources :',
    error: 'Désolé, j\'ai rencontré une erreur. Veuillez réessayer.',
    close: 'Fermer le chat',
    clear: 'Effacer le chat',
    emptyStateGreeting: '👋 Bonjour ! Je suis votre tuteur IA.',
    emptyStateHint: 'Posez-moi des questions sur le contenu du manuel !',
    selectedTextHint: '💡 Je vois que vous avez sélectionné du texte. Interrogez-moi à ce sujet !',
    aiResponseNote: 'L\'IA répond en anglais',
  },

  // Arabic (العربية) - RTL
  ar: {
    title: 'المعلم الذكي',
    placeholder: 'اطرح سؤالاً حول الكتاب...',
    send: 'إرسال',
    typing: 'الذكاء الاصطناعي يفكر...',
    selectedText: 'المحدد:',
    sources: 'المصادر:',
    error: 'عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.',
    close: 'إغلاق المحادثة',
    clear: 'مسح المحادثة',
    emptyStateGreeting: '👋 مرحباً! أنا معلمك الذكي.',
    emptyStateHint: 'اسألني أي شيء عن محتوى الكتاب!',
    selectedTextHint: '💡 أرى أنك حددت بعض النص. اسألني عنه!',
    aiResponseNote: 'الذكاء الاصطناعي يجيب بالإنجليزية',
  },

  // Urdu (اردو) - RTL
  ur: {
    title: 'اے آئی ٹیوٹر',
    placeholder: 'نصابی کتاب کے بارے میں سوال پوچھیں...',
    send: 'بھیجیں',
    typing: 'اے آئی سوچ رہا ہے...',
    selectedText: 'منتخب شدہ:',
    sources: 'ذرائع:',
    error: 'معذرت، ایک خرابی پیش آگئی۔ براہ کرم دوبارہ کوشش کریں۔',
    close: 'چیٹ بند کریں',
    clear: 'چیٹ صاف کریں',
    emptyStateGreeting: '👋 السلام علیکم! میں آپ کا اے آئی ٹیوٹر ہوں۔',
    emptyStateHint: 'نصابی کتاب کے مواد کے بارے میں مجھ سے کچھ بھی پوچھیں!',
    selectedTextHint: '💡 میں دیکھ سکتا ہوں کہ آپ نے کچھ متن منتخب کیا ہے۔ اس کے بارے میں پوچھیں!',
    aiResponseNote: 'اے آئی انگریزی میں جواب دیتا ہے',
  },
};

/**
 * Get translations for a specific locale
 * Falls back to English if locale is not supported
 */
export function getTranslations(locale: string): ChatWidgetStrings {
  const supportedLocale = locale as Locale;
  return translations[supportedLocale] || translations.en;
}

/**
 * Check if a locale uses RTL (right-to-left) direction
 */
export function isRTL(locale: string): boolean {
  return locale === 'ar' || locale === 'ur';
}

export default translations;
