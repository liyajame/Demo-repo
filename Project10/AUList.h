#define MAXSIZE 202

struct hotelbooking {
int is_canceled;  //time
int lead_time;   //amount
int arrival_date_year; //fraudclass  	
};

class AUList
{
public:

    AUList(); // Constructor

    void MakeEmpty();  // Returns the list to the empty state.

    bool IsFull() const; //Determines whether list is full. (Precondition -- list has been initialized).  Return value of "True" indicates class is full.

    int GetLength() const; //Determines the number of elements in list.

    void PutItem(hotelbooking); //Adds the item to the list.

    void ResetList();  //Initializes iterator's current position for an iteration through the list.

    hotelbooking GetNextItem(); //Gets the next element in the list.

    bool HasNextItem();

    void PrintList();  //Print all elements of the list in a readable format.



private:
    int length;
    hotelbooking ListItems[MAXSIZE];
    int currentPos;
};

