#include <pthread.h>
#include <iostream>
#include <wann/WiSARD.hpp>
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <time.h>
#include <tuple>
#include <random>
#include <chrono>
#include <map>
#include <assert.h>

using namespace wann;
using namespace std;

double accuracyScore(vector<string> y, vector<string> ypred)
{

    assert(y.size() == ypred.size());
    double count = 0.0;
    for(int i = 0; i < y.size(); i++)
    {
        if(y[i] == ypred[i])
        {
            count = count + 1;
        }
    }
    return count/y.size();
}


vector<int> split(string str, char delimiter) {
    vector<int> internal;
    stringstream ss(str); // Turn the string into a stream.
    string tok;
    while(getline(ss, tok, delimiter)) {
        internal.push_back( stoi(tok));
    }
    return internal;
}

vector<string> split_str(string str, char delimiter) {
    vector<string> internal;
    stringstream ss(str); // Turn the string into a stream.
    string tok;
    while(getline(ss, tok, delimiter)) {
        internal.push_back( tok );
    }
    return internal;
}


tuple< vector<vector<int>>, vector<string>> loadData(string XFile, string yFile)
{
    string line;
    ifstream input(XFile);
    ifstream annotation (yFile);
    vector<vector<int>> X;
    vector<string> y;
    //reading X
    if (input.is_open())
    {
        while(getline(input, line))
        {
            X.push_back(split(line, ','));
        }
        input.close();
    }
    //reading y
    getline(annotation, line);
    y = split_str(line, ',');
    return make_tuple(X,y);
}

extern "C" double object_function(int numBitsAddr, 
                                  float confidenceThreshold, 
                                  float ssthreshold, 
                                  int onlineMax,
                                  int init_size)
{
    float confidence;
    float prob0;
    float prob1;

    vector<vector<int>> X;
    vector<string> y;

    string XFile = "data/spam_nominal_X.csv";
    string yFile= "data/spam_nominal_y.csv";

    tie(X, y) = loadData(XFile, yFile);

    vector<vector<int>>::const_iterator first = X.begin();
    vector<vector<int>>::const_iterator mid = X.begin() + init_size;
    vector<vector<int>>::const_iterator last = X.begin() + X.size();

    vector<string>::const_iterator first_y = y.begin();
    vector<string>::const_iterator mid_y = y.begin() + init_size;
    vector<string>::const_iterator last_y = y.begin() + y.size();


    vector<vector<int>> X_train(first, mid);
    vector<vector<int>> X_test(mid, last);

    vector<string> y_train(first_y, mid_y);
    vector<string> y_test(mid_y, last_y);
    vector<unordered_map<string, float>> ypredproba;
    vector<string> ypred;


    // parameters:
    // WiSARD(int numBitsAddr,
    //        bool useBleaching=true,
    //        float confidenceThreshold=0.1,
    //        int defaultBleaching_b=1,
    //        bool randomizePositions=true,
    //        bool isCummulative=true,
    //        bool ignoreZeroAddr=false,
    //        int onlineMax = 2);
    WiSARD * w = new WiSARD(numBitsAddr, true, confidenceThreshold, 1, true, true, true, onlineMax);

    w->fit(X_train, y_train);
    int counter = 0;

    for(int i = 0; i < X_test.size(); i++)
    {
        
        vector<vector<int>> tempX;
        tempX.push_back(X_test[i]);
        vector<string> temp_ypred;


        ypredproba = w->predictProba(tempX);
        prob0 = ypredproba[0]["0"];
        prob1 = ypredproba[0]["1"];

        float maxprob = max(prob0,prob1);
        float minprob = min(prob0,prob1);

        confidence = 0;

        if(maxprob != 0)
        {
            confidence = 1 - (minprob / maxprob);
        }
        // cout << confidence << endl;
        
        if(prob0 > prob1)
        {
            ypred.push_back("0");
            if (confidence > ssthreshold){
                temp_ypred.push_back("0");
                w->onFit(tempX, temp_ypred);
            }

        }
        if(prob0 < prob1)
        {
            ypred.push_back("1");
            if (confidence > ssthreshold){
                temp_ypred.push_back("1");
                w->onFit(tempX, temp_ypred);
            }
        }
        if(prob0 == prob1){
            counter++;
            ypred.push_back("0");
        }
        

    }
    cout << "== : " << counter << endl;
    return accuracyScore(y_test, ypred);

}

int main(int argc, char** argv)
{
    // ['18', '0.348885724015', '0.01', '26', '1835']

    cout << object_function(10, 0.1, 0.1, 10, 3000) << endl;
    return 0;

}
