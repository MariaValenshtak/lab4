from googletrans import Translator, LANGUAGES


async def TransLate(text: str, scr: str, dest: str) -> str:
    try:
        async with Translator() as translator:
            result = await translator.translate(text, src=scr, dest=dest)
            return result.text
    except Exception as e:
        return f"Помилка: {e}"


async def LangDetect(text: str, set: str = "all") -> str:
    try:
        async with Translator() as translator:
            result = await translator.detect(text)
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


async def LanguageList(out: str = "screen", text: str = "") -> str:
    try:
        rows = []
        async with Translator() as translator:
            for i, (code, name) in enumerate(LANGUAGES.items(), start=1):
                translated = ""
                if text:
                    try:
                        result = await translator.translate(text, src="auto", dest=code)
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
            with open("languages_gtrans4.txt", "w", encoding="utf-8") as f:
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