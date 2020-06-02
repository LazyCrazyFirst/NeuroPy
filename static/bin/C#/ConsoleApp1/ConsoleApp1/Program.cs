using System;
using System.Collections.Generic;
using System.IO;

namespace ConsoleApp1
{
    class Program
    {
        public static void Raschet(Dictionary<string, string> geting)
        {
            //Переменные
            string var1 = "Привет";
            int var2 = 18;
            string var3 = "FUCK YOU";

            string[] variables = { nameof(var1), nameof(var2), nameof(var3) }; //Записываем в массив имена переменных
            string[] values = { Convert.ToString(var1), Convert.ToString(var2), Convert.ToString(var3) }; //Записываем в массив значения переменных

            Writing_And_Output_From_A_File.Writing_To_A_File(variables, values); //Вызов метода записи переменных в файл


            Console.WriteLine("Пока");
        }

        public static void Demo(Dictionary<string, string> geting)
        {
            Console.WriteLine("Привет");
        }
        static void Main(string[] args)
        {

            Writing_And_Output_From_A_File.Geting(); //Вызов метода считывания переменных из файла

        }

    }
}
