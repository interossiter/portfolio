using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace FileMover
{
	class Program
	{
		static void Main(string[] args)
		{

			//0 = SOURCE FOLDER
			//1 = DESTINATION
			//2 = EXTENSION
			//3 = DAYS BACK

			int nDaysBack = int.MaxValue;

			nDaysBack = Math.Abs(int.Parse(args[3]));

			string[] files = Directory.GetFiles(args[0]);
			foreach (string i in files)
			{
				
				//Console.WriteLine(i);

				FileInfo FileProps = new FileInfo(i);

				//Console.WriteLine(FileProps.LastWriteTime.ToShortDateString());

				TimeSpan ts = DateTime.Now.Subtract(FileProps.LastWriteTime);

				if (ts.TotalDays >= nDaysBack && FileProps.Extension.ToUpper().ToString() == args[2].ToUpper().ToString())
				{

					//Console.WriteLine("Flush it!!!!!!!!!!");

					//Console.WriteLine(args[1].ToString());

					//Console.WriteLine(FileProps.Name.ToString());

					string sDest = args[1].Replace("\\", "\\\\").ToString() + "\\\\" + FileProps.Name.Replace("\\", "\\\\").ToString();

					Console.WriteLine(sDest);

					//Console.WriteLine("End flush....");

					FileProps.MoveTo(sDest);

				}

			}

		}

	}

}
