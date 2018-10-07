// basic file input output

# include <iostream>
# include <fstream>
#include <sstream>

using namespace std;

const int nodes = 200;
const int attributes = 5;
string data[nodes][attributes];	


void ReadFile(string filename)
{
	ifstream dataFile(filename);
	/*if(!dataFile)
	{
		cout << "file is not opened" << endl;

	}



	if(dataFile.is_open())
	{
		int i =0;
        string line;

        while(getline(dataFile, line))
        {
         //cout << line << endl;
         stringstream ss(line);
         for (int j=0; j<attributes; j++)
         {
         	getline(ss, data[i][j], ',');
         }	
         i++;
        }
        
	}

	for(int i=0; i<200; i++)
	{
		for(int j=0; j<5; j++)
		{
			cout << data[i][j] << ",";
		}
		cout << endl;
	}
	return 0;
	*/
    
} 				

int main()
{
    ReadFile("data.txt");	
	return 0;

}