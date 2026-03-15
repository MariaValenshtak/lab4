import sys

if sys.version_info >= (3, 13):

    def TransLate(text: str, scr: str, dest: str) -> str:
        return "Помилка: googletrans==3.1.0a0 не підтримується для Python 3.13 і вище"

    def LangDetect(text: str, set: str = "all") -> str:
        return "Помилка: googletrans==3.1.0a0 не підтримується для Python 3.13 і вище"

    def CodeLang(lang: str) -> str:
        return "Помилка: googletrans==3.1.0a0 не підтримується для Python 3.13 і вище"

    def LanguageList(out: str = "screen", text: str = "") -> str:
        return "Помилка: googletrans==3.1.0a0 не підтримується для Python 3.13 і вище"

else:
    from googletrans import Translator, LANGUAGES

    def TransLate(text: str, scr: str, dest: str) -> str:
        try:
            translator = Translator()
            result = translator.translate(text, src=scr, dest=dest)
            return result.text
        except Exception as e:
            return f"Помилка: {e}"

    def LangDetect(text: str, set: str = "all") -> str:
        try:
            translator = Translator()
            result = translator.detect(text)
            lang_name = LANGUAGES.get(result.lang, result.lang)
            confidence = result.confidence

            if set == "lang":
                return f"{lang_name} ({result.lang})"
            elif set == "confidence":
                return str(confidence)
            elif set == "all":
                return f"Мова: {lang_name} ({result.lang}), довіра: {confidence}"
            else:
                return "Помилка: неправильний параметр set"
        except Exception as e:
            return f"Помилка: {e}"

    def CodeLang(lang: str) -> str:
        try:
            lang = lang.lower()

            if lang in LANGUAGES:
                return LANGUAGES[lang]

            for code, name in LANGUAGES.items():
                if name.lower() == lang:
                    return code

            return "Помилка: мову не знайдено"
        except Exception as e:
            return f"Помилка: {e}"

    def LanguageList(out: str = "screen", text: str = "") -> str:
        try:
            rows = []
            translator = Translator()

            for i, (code, name) in enumerate(LANGUAGES.items(), start=1):
                translated = ""
                if text:
                    try:
                        result = translator.translate(text, src="auto", dest=code)
                        translated = result.text
                    except Exception:
                        translated = "error"

                if text:
                    rows.append((i, name.title(), code, translated))
                else:
                    rows.append((i, name.title(), code))

            if out == "screen":
                if text:
                    print(f"{'N':<4}{'Language':<20}{'ISO-639 code':<15}{'Text'}")
                    print("-" * 70)
                    for row in rows:
                        print(f"{row[0]:<4}{row[1]:<20}{row[2]:<15}{row[3]}")
                else:
                    print(f"{'N':<4}{'Language':<20}{'ISO-639 code':<15}")
                    print("-" * 40)
                    for row in rows:
                        print(f"{row[0]:<4}{row[1]:<20}{row[2]:<15}")

            elif out == "file":
                with open("languages_gtrans3.txt", "w", encoding="utf-8") as f:
                    if text:
                        f.write(f"{'N':<4}{'Language':<20}{'ISO-639 code':<15}{'Text'}\n")
                        f.write("-" * 70 + "\n")
                        for row in rows:
                            f.write(f"{row[0]:<4}{row[1]:<20}{row[2]:<15}{row[3]}\n")
                    else:
                        f.write(f"{'N':<4}{'Language':<20}{'ISO-639 code':<15}\n")
                        f.write("-" * 40 + "\n")
                        for row in rows:
                            f.write(f"{row[0]:<4}{row[1]:<20}{row[2]:<15}\n")
            else:
                return "Помилка: out має бути 'screen' або 'file'"

            return "Ok"
        except Exception as e:
            return f"Помилка: {e}"