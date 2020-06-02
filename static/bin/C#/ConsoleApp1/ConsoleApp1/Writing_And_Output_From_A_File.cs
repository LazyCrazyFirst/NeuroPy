using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;

namespace ConsoleApp1
{
    class Writing_And_Output_From_A_File
    {
        public static void Geting()
        {
            string pathToFile = "variables.txt"; //Указываем путь к файлу
            string readAllFile = File.ReadAllText(pathToFile); //Сохраняем весь файл в переменную
            string[] j = readAllFile.Split("\n"); //Загоняем в массив каждую строку из файла
            Dictionary<string, string> geting = new Dictionary<string, string>(j.Length); //Создаём словарь
                                                                                          //Пробегаемся по каждой строке
            foreach (string i in j)
            {
                //удаление \r
                string str = i;
                string find = "\r";
                if (str.IndexOf(find) != 0)
                    try
                    {
                        str = str.Remove(str.IndexOf(find), 1);
                    }
                    catch
                    {

                    }
                string[] h = str.Split(" "); //Пробегаемся по каждому слову в строке
                string value = "";
                string variable = h[0]; //В качестве имени "переменной" берём первое слово

                //Берём все остальные слова, после имени "переменной", это и будет значение переменной
                foreach (string el in h)
                {
                    if (el != variable)
                    {
                        value += el + " ";
                    }

                }

                //Убираем \n в начале переменных
                /*if (geting.Count != 0)
                {
                    variable = variable.Remove(0, 1);
                }*/

                value = value.Remove(value.Length - 1, 1); //Убираем пробелы в конце значений
                geting.Add(variable, value); //Добавляем в словарь
            }

            //Вызов методов
            foreach (KeyValuePair<string, string> keyValue in geting)
            {
                if (keyValue.Value == "Method")
                {
                    switch (keyValue.Key)
                    {
                        case "Raschet":
                            Program.Raschet(geting);
                            break;

                        case "Demo":
                            Program.Demo(geting);
                            break;
                    }
                }
            }
        }



        //Метод записи переменных в файл
        public static void Writing_To_A_File(string[] variables, string[] values)
        {
            //Создаём словарь 
            Dictionary<string, string> variable = new Dictionary<string, string>(values.Length);

            //Записываем в словарь имена и значения переменных
            for (int i = 0; i < values.Length; i++)
            {
                variable.Add(variables[i], values[i]);
            }

            FileStream file = new FileStream("variables.txt", FileMode.Create); //создаем файловый поток
            StreamWriter writer = new StreamWriter(file); //создаем «потоковый писатель» и связываем его с файловым потоком

            int k = 0;
            foreach (var value in variable)
            {
                k += 1;

                string varia = (value.Key + " " + value.Value); //Записываем в строку имя и значение переменной

                //Если у нас последняя строка перенос не ставим
                if (values.Length != k)
                {
                    varia += "\n";
                }

                writer.Write(varia); //записываем в файл
            }
            writer.Close(); //закрываем поток. Не закрыв поток, в файл ничего не запишется
        }
    }
}
