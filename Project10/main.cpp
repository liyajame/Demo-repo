#include "AUList.h"
#include <fstream>
#include <sstream>
#include <iostream>
using namespace std;

AUList csvtoAUList(string csvfile) { //convert a csv file to a list structure
    AUList retCCList;
	ifstream ReadFile(csvfile); //open the csv file for reading
    string line, curvalue;
	getline(ReadFile, line); //throw away the first line (column names)
    while (getline(ReadFile,line)) {        
        stringstream ss(line); //turn the line into a string-stream
        int fielditer=0;
        hotelbooking newrec;
		while(getline(ss, curvalue, ',')){ //Separate each variable per sample from the comma separator
            switch (fielditer) { //We need to explicitly convert values to the appropriate type (stoi=integer, stod=double)
            	case 0: newrec.is_canceled=stoi(curvalue); break;
            	case 1: newrec.lead_time=stod(curvalue); break;
            	case 2: newrec.arrival_date_year =stoi(curvalue); break;
			}
            fielditer++;
        }
        retCCList.PutItem(newrec);
    }
    return retCCList;
}

int main(int argc, char** argv) {
	AUList hotelbooking=csvtoAUList("database_hotel.csv");
	hotelbooking.PrintList(); //Print the data record-by-record
}
    
