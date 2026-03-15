from deep_translator import GoogleTranslator
from langdetect import detect, detect_langs

LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)


async def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        translated = GoogleTranslator(source=scr, target=dest).translate(text)
        return translated
    except Exception as e:
        return f"Помилка: {e}"


async def LangDetect(text: str, set: str = "all") -> str:
    try:
        lang_code = detect(text)
        probs = detect_langs(text)
        confidence = probs[0].prob if probs else 0.0

        lang_name = lang_code
        for name, code in LANGUAGES.items():
            if code == lang_code:
                lang_name = name
                break

        if set == "lang":
            return f"{lang_name} ({lang_code})"
        elif set == "confidence":
            return str(confidence)
        elif set == "all":
            return f"Мова: {lang_name} ({lang_code}), довіра: {confidence}"
        else:
            return "Помилка: неправильний параметр set"
    except Exception as e:
        return f"Помилка: {e}"


def CodeLang(lang: str) -> str:
    try:
        lang = lang.lower()

        if lang in LANGUAGES:
            return LANGUAGES[lang]

        for name, code in LANGUAGES.items():
            if code == lang:
                return name

        return "Помилка: мову не знайдено"
    except Exception as e:
        return f"Помилка: {e}"


async def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        rows = []

        for i, (name, code) in enumerate(LANGUAGES.items(), start=1):
            translated = ""
            if text:
                try:
                    translated = GoogleTranslator(source="auto", target=code).translate(text)
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
            with open("languages_deep.txt", "w", encoding="utf-8") as f:
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