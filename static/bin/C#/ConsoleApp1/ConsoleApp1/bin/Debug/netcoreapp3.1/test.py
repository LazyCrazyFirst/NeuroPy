import os
from Writing_And_Output_From_A_File import writing_to_a_file, reading_from_a_file

# Переменные
var1 = 'hello'
var2 = 4
var3 = 'Лох'

# Словарь с переменными для записи в файл
variables = ['var1', 'var2', 'var3', 'Raschet', 'Demo']  # Запись имён
value = [var1, var2, var3, 'Method', 'Method']  # Запись значений

# Вызов функции добавления переменных в файл
writing_to_a_file(variables, value)

# Вызов функции чтения переменных
# print(reading_from_a_file())

# Запуск C# файла
# os.system('ConsoleApp1.exe')
