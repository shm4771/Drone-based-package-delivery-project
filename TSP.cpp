# include <stdio.h>
# include <iostream>
# include <typeinfo>

using namespace std;


int nodes = 5;
//int set[nodes] = {0,1,2,3};      //set which is container of all child ids of 0th node
int set[nodes] = {0,1,2,3,4};

//Test data ---hardcoded
//int cost[4][4] = {{0,4,1,3},{4,0,2,1},{1,2,0,5},{3,1,5,0}};
int cost[nodes][nodes] = {{0,4,3,1,8},{4,0,2,2,4},{3,2,0,3,2},{1,2,3,0,2},{8,4,2,2,0}};
//int map[4][4][4];
int map[nodes][nodes][nodes]; //nodes, parenIDm self



//function to remove an elemnt from array and return modified array
//----->takes a array, it's size and the element which needs to be removed as inputs
int *removeData(int size, int array[], int element)
{
    bool isRemoved = 0;
    int *Newarray = new int[size-1];
    for(int i=0;i<size;i++)
    {
        if(element != array[i] && isRemoved == 0)
        {
            Newarray[i] = array[i];
            //cout << Newarray[i] << ",";
        }
        else if(element != array[i] && isRemoved == 1)
        {
            Newarray[i-1] = array[i];
            //cout << Newarray[i-1] << ",";
        }
        else
        {

            isRemoved = 1;
        }

    }
    //cout << endl;
    return Newarray;
}


//function to find the minimum element in a array and stores the childId in a memory map who was selected in comparison step

int min(int parentId, int Index, int size, int sum[], int array[])
{
    int k; //variable which contain the index of the child branch cost which gives minimum cost 
    int temp = sum[0];
    if(size == 1){map[size][parentId][Index]= array[0];return sum[0];}
    else
    {
        for(int i=1;i<size;i++)
        {
            if(temp>= sum[i]){k=i; temp = sum[i];}

        }
        //cout << "The min size is" << temp <<endl;
        map[size][parentId][Index]= array[k];
        return temp;

    }

}


//Function who calculate total minimum cost in recursive calls
int minSum(int parentId, int nodeIndex, int size, int array[])
{
    //cout << "size is " << size << endl;
    //size is the length of a set which contain child ids
    if (size == 0){return cost[nodeIndex][0];}
    else
    {
        
        int node_sum[size];  //array to collect the costs from all child branches of the node

        //loop for calculating costs from all child branches of node "nodeIndex"
        for(int k=0;k<size;k++)
        {
            int j = array[k];
            //cout << "size: " << size << endl;
            int *newArray = removeData(size, array, j);
            node_sum[k] = cost[nodeIndex][j] + minSum(nodeIndex, j, size-1, newArray);        
            //cout << "sum" << k << "is" << sum[k]<<endl;
        }
        return min(parentId, nodeIndex, size, node_sum, array); //min function to select the minimum cost from the costs of child branches
        
    }

}



int main()
{

    int sum;
    int *newArray = removeData(nodes, set, 0);

    //function args - parent id, self id, size of set, set
    sum = minSum(0, 0, nodes-1, newArray);
    cout << "optimum total cost is: "<<sum << endl;

    int path[5];  //array for storing the optimal path
    int parentId=0;
    int selfId=0;
    int size = nodes-1;
/*
    for(int i=0;i<4;i++)
    {
        for(int j=0;j<4;j++)
        {
            for(int k=0;k<4;k++)
            {
                cout <<"i"<<i<<" "<<"j"<<j<<" "<<"k"<<k<<" "<<"NextIndex"<< map[i][j][k]<<endl;
            }
        }
    }
*/
    // displaying the optimal path
    cout << "The chosen path will be: ";
    for(int i=0;i<nodes+1;i++)
    {
        path[i] = map[size][parentId][selfId];  
        size --;
        parentId = selfId;
        selfId = path[i];
        cout<< " -> "<<parentId ;

    }
    cout << endl;
    cout << "Cheers !!"<<endl;


    //cout << typeid(newArray).name() << endl;

//    
//    for(int i=0;i<3;i++){
//        cout << newArray[i] << endl;
//    }


}