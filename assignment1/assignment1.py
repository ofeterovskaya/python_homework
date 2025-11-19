# Write your code here.
# Task 1: Hello
def hello():
  return "Hello!"
print(hello())

# Task 2: Greet with a Formatted String
def greet(name):
  return(f"Hello, {name}!")
print(greet("Oksana"))

# Task 3: Calculator
def calc(a, b, operation="multiply"):
  try:
    if operation == "add":
      result = a + b
    elif operation == "subtract":
      result  = a - b
    elif operation == "divide":
      result = a / b
    elif operation == "modulo":
      result = a % b
    elif operation == "multiply":
      result = a * b
    elif operation == "int_divide":
      result = a // b
    elif operation == "power":
      result = a ** b
    return result
  except ZeroDivisionError:
        return "You can't divide by 0!"
  except TypeError:
        return "You can't multiply those values!"
  
print(calc(2, 3, "add"))
print(calc(2, 3, "subtract"))
print(calc(6, 3, "divide"))
print(calc(7, 3, "modulo"))
print(calc(4, 5, "multiply"))
print(calc(7, 3, "int_divide"))
print(calc(2, 3, "power"))
print(calc(2, 0, "divide"))
print(calc("a", "b", "multiply"))

# Task 4: Data Type Conversion
def data_type_conversion(a, conversion_type):
  try:
    if conversion_type == "int":
      return int(a)
    elif conversion_type == "float":
      return float(a)
    elif conversion_type == "str":
      return str(a)
  except ValueError:
    return f"You can't convert {a} into a {conversion_type}."
print(data_type_conversion("123", "int"))
print(data_type_conversion("12.34", "float"))
print(data_type_conversion(56, "str"))
print(data_type_conversion("banana", "int"))

# Task 5: Grading System, Using *args
def grade(*grades):
  try:
    average = sum(grades) / len(grades)
  except Exception:
    return "Invalid data was provided."
  average = sum(grades) / len(grades)
  if average >= 90:
    return "A"
  elif average >= 80:
    return "B"
  elif average >= 70:
    return "C"
  elif average >= 60:
    return "D"
  else:
    return "F"

print(grade(85, 90, 78))
print(grade(60, 65, 70))
print(grade())
print(grade("abc", 100))

# Task 6: Use a For Loop with a Range
def repeat(text, count):
    result = ""  # to store the result
    for _ in range(count):
        result += text
    return result

print(repeat("Hi", 3))
print(repeat("A", 5))
print(repeat("", 4))


# Task 7: Student Scores, Using **kwargs
def student_scores(mode, **kwargs):
    if mode == "mean":
        return sum(kwargs.values()) / len(kwargs)
    elif mode == "best":
        return max(kwargs, key=kwargs.get)
    
print(student_scores("mean", Alice=85, Bob=90, Charlie=78))
print(student_scores("best", Alice=85, Bob=90, Charlie=78))

# Task 8: Titleize, with String and List Operations
def titleize(text):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = text.split()
    result_words = []

    for i, word in enumerate(words):
        lower_word = word.lower()
        if i == 0 or i == len(words) - 1: # first letter and last letter always capitalize
            result_words.append(lower_word.capitalize())        
        elif lower_word in little_words: # small words remain lowercase
            result_words.append(lower_word)        
        else:
            result_words.append(lower_word.capitalize()) # all other words capitalize
    return " ".join(result_words)

print(titleize("code the dream"))
print(titleize("python programming language"))
print(titleize("a tale of two princesses"))

# Task 9: Hangman, with more String Operations
def hangman(text, guess):
    result = ""
    for char in text:
        if char in guess:
            result += char
        else:
            result += "_"
    return result
print(hangman("alphabet", "ab"))
print(hangman("python", "pt"))
print(hangman("banana", "an"))

# Task 10: Pig Latin, Another String Manipulation Exercise
def pig_latin(english):
    vowels = "aeiou"
    words = english.split()
    pig_latin_words = []
    for word in words:
        lower_word = word.lower()
        if lower_word[0] in vowels: # if starts with a vowel
            pig_latin_word = lower_word + "ay"
        else:
            i = 0
            while i < len(lower_word) and lower_word[i] not in vowels:
                if lower_word[i] == "q" and i + 1 < len(lower_word) and lower_word[i + 1] == "u":
                    i += 2
                    break
                i += 1
            pig_latin_word = lower_word[i:] + lower_word[:i] + "ay"
        
        pig_latin_words.append(pig_latin_word)

    return " ".join(pig_latin_words)
print(pig_latin("apple"))
print(pig_latin("python"))
print(pig_latin("code the dream"))
print(pig_latin("alphabet"))
print(pig_latin("queen"))