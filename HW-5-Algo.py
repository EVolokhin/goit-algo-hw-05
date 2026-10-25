import timeit

# 1. Алгоритм Боєра-Мура

def build_shift_table(pattern):
    """Будуємо таблицю зсувів за останнім входженням символу."""
    table = {}
    length = len(pattern)
    for i in range(length - 1):
        table[pattern[i]] = length - 1 - i
    return table

def boyer_moore(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    pattern_len = len(pattern)
    text_len = len(text)

    while i <= text_len - pattern_len:
        j = pattern_len - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i  # Знайдено підрядок
        
        # Зсув за допомогою таблиці або довжиною підрядка
        shift = shift_table.get(text[i + pattern_len - 1], pattern_len)
        i += shift
    return -1

# 2. Алгоритм Кнута-Морріса-Пратта (KMP)

def compute_lps(pattern):
    """Обчислення масиву найдовшого префікса-суфікса (LPS)."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = 0  # індекс для text
    j = 0  # індекс для pattern
    text_len = len(text)
    pattern_len = len(pattern)

    while i < text_len:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == pattern_len:
            return i - j  # Знайдено підрядок
        elif i < text_len and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# 3. Алгоритм Рабіна-Карпа

def rabin_karp(text, pattern, d=256, q=101):
    pattern_len = len(pattern)
    text_len = len(text)
    h = pow(d, pattern_len - 1) % q
    p = 0
    t = 0

    if pattern_len > text_len:
        return -1

    # Обчислення хешу для підрядка та першого вікна тексту
    for i in range(pattern_len):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(text_len - pattern_len + 1):
        if p == t:
            if text[i:i + pattern_len] == pattern:
                return i  # Знайдено підрядок
        
        if i < text_len - pattern_len:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + pattern_len])) % q
            if t < 0:
                t += q
    return -1


# Бенчмаркінг за допомогою timeit

def run_benchmarks(text, existing_pattern, fake_pattern, iterations=10):
    algorithms = {
        "Боєра-Мура": boyer_moore,
        "Кнута-Морріса-Пратта": kmp_search,
        "Рабіна-Карпа": rabin_karp
    }
    
    results = {}
    
    for name, func in algorithms.items():
        # Вимірюємо час для існуючого підрядка
        timer_exist = timeit.Timer(lambda: func(text, existing_pattern))
        time_exist = timer_exist.timeit(number=iterations) / iterations
        
        # Вимірюємо час для вигаданого підрядка
        timer_fake = timeit.Timer(lambda: func(text, fake_pattern))
        time_fake = timer_fake.timeit(number=iterations) / iterations
        
        results[name] = {
            "існуючий": time_exist,
            "вигаданий": time_fake
        }
        
    return results

if __name__ == "__main__":
    # Завантаження статей (з кодуванням utf-8)
    try:
        with open("стаття_1.txt", "r", encoding="cp1251") as f1:
            article1 = f1.read()
        with open("стаття_2.txt", "r", encoding="cp1251") as f2:
            article2 = f2.read()
    except FileNotFoundError:
        print("Помилка: Переконайтеся, що файли стаття_1.txt та стаття_2.txt знаходяться у папці зі скриптом.")
        exit()

    # Вкажіть свої підрядки або змініть за потреби
    pattern1_exist = "алгоритм"       # Існуючий підрядок у статті 1
    pattern1_fake = "квантовий комп'ютер" # Вигаданий підрядок у статті 1

    pattern2_exist = "база даних"     # Існуючий підрядок у статті 2
    pattern2_fake = "нейронна мережа" # Вигаданий підрядок у статті 2

    print("=== Результати тестування для Статті 1 ===")
    res1 = run_benchmarks(article1, pattern1_exist, pattern1_fake)
    for alg, times in res1.items():
        print(f"{alg:22} | Існуючий: {times['існуючий']:.6f} с | Вигаданий: {times['вигаданий']:.6f} с")

    print("\n=== Результати тестування для Статті 2 ===")
    res2 = run_benchmarks(article2, pattern2_exist, pattern2_fake)
    for alg, times in res2.items():
        print(f"{alg:22} | Існуючий: {times['існуючий']:.6f} с | Вигаданий: {times['вигаданий']:.6f} с")