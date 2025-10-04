import string
from collections import Counter #to zliczania liter(potrzebne potem do rozkladu chi^2)

texts = {
    "english": "This is a sample text in English, written to be around fifty words long. English is a widely spoken language, used for communication in many different parts of the world. Learning English can open up many opportunities, both professionally and personally. Practice reading and speaking it daily to improve your skills.",
    "polish": "To przykladowy tekst w jezyku polskim, liczacy okolo piecdziesieciu slow. Jezyk angielski jest powszechnie uzywanym jezykiem, uzywanym do komunikacji w wielu czesciach swiata. Nauka angielskiego moze otworzyc wiele mozliwosci, zarowno zawodowych, jak i osobistych. Cwicz czytanie i mowienie w tym jezyku codziennie, aby poprawic swoje umiejetnosci.",
    "spanish": "Este es un texto de muestra en Espana, escrito para unas cincuenta palabras. El ingles es un idioma ampliamente hablado y utilizado para la comunicacion en muchas partes del mundo. Aprender ingles puede abrirte muchas oportunidades, tanto profesionales como personales. Practica la lectura y la conversacion a diario para mejorar tus habilidades."
}

shifts = {
    "english": 5,
    "polish": 7,
    "spanish": 13
}

alphabet = string.ascii_uppercase #wszystkie wielkiE litery (do sprawdzania czy znak jest litera)

def caesar_encrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            is_lower = ch.islower() #sprawdzamy i zapamietujemy czy mala zeby potem moc zmienic
            ch_up = ch.upper() #wszytskie dajemy na duze
            idx = alphabet.index(ch_up) #indeksujemy nasze litery
            new_char = alphabet[(idx + shift) % 26] #znak po zmianie
            result += new_char.lower() if is_lower else new_char
        else:
            result += ch
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


freqs = {
    "english": {
        'A':8.167,'B':1.492,'C':2.782,'D':4.253,'E':12.702,'F':2.228,'G':2.015,'H':6.094,'I':6.966,
        'J':0.153,'K':0.772,'L':4.025,'M':2.406,'N':6.749,'O':7.507,'P':1.929,'Q':0.095,'R':5.987,
        'S':6.327,'T':9.056,'U':2.758,'V':0.978,'W':2.360,'X':0.150,'Y':1.974,'Z':0.074
    },
    "polish": { 
        'A':8.91,'B':1.47,'C':3.96,'D':3.25,'E':7.66,'F':0.30,'G':1.42,'H':1.08,'I':8.21,
        'J':2.28,'K':3.51,'L':2.10,'M':2.80,'N':5.52,'O':7.75,'P':3.13,'Q':0.00,'R':4.69,
        'S':4.32,'T':3.98,'U':2.50,'V':0.04,'W':4.65,'X':0.02,'Y':3.76,'Z':5.64
    },
    "spanish": {
        'A':12.53,'B':1.42,'C':4.68,'D':5.86,'E':13.68,'F':0.69,'G':1.01,'H':0.70,'I':6.25,
        'J':0.52,'K':0.02,'L':4.97,'M':3.15,'N':6.71,'O':8.68,'P':2.51,'Q':0.88,'R':6.87,
        'S':7.98,'T':4.63,'U':3.93,'V':0.90,'W':0.01,'X':0.22,'Y':1.01,'Z':0.47
    }
}

#zliczanie wystepujacych liter 
def count_letters(text):
    filtered = [c.upper() for c in text if c.upper() in alphabet]
    return Counter(filtered), len(filtered)

def chi_squared(observed, total, expected_freq):
    chi2 = 0
    for letter in alphabet:
        obs = observed.get(letter, 0) 
        #szacowana ilosc wystpien w tekscie (na podstawie statystycznych wystapien liter i dlugoosci tekstu)
        exp = total * (expected_freq.get(letter, 0) / 100)
        if exp > 0:
            #χ² = Σ [(obserwowane - oczekiwane)² / oczekiwane]
            chi2 += (obs - exp) ** 2 / exp
    return chi2

def break_cipher(ciphertext, language):
    best_shift = 0
    best_score = float('inf')
    for shift in range(26):
        #deszyfurjemy z danym przesunieciem
        candidate = caesar_decrypt(ciphertext, shift)
        counts, total = count_letters(candidate)
        score = chi_squared(counts, total, freqs[language])
        #sprawdzenie zeby ch2 bylo jak najmniejsze
        if score < best_score:
            best_score = score
            best_shift = shift
    return best_shift

# Dla każdego języka: szyfrujemy → łamiemy klucz → deszyfrujemy
for lang, text in texts.items():
    print("\n==========================")
    print(f"Język: {lang.upper()}")
    print("==========================")
    shift = shifts[lang]
    encrypted = caesar_encrypt(text, shift)
    print(f"Tekst oryginalny:   {text}")
    print(f"Tekst zaszyfrowany: {encrypted}")

    found_shift = break_cipher(encrypted, lang)
    decrypted = caesar_decrypt(encrypted, found_shift)

    print(f"Złamany klucz:      {found_shift}")
    print(f"Tekst odszyfrowany: {decrypted}")
