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

using namespace wann;
using namespace std;

double deviation(vector<float> v, float ave)
{
    double E=0;
    // Quick Question - Can vector::size() return 0?
    double inverse = 1.0 / static_cast<double>(v.size());
    for(unsigned int i=0;i<v.size();i++)
    {
        E += pow(static_cast<double>(v[i]) - ave, 2);
    }
    return sqrt(inverse * E);
}

float average(vector<float> v)
{
    float sum=0;
    for(int i=0;i<v.size();i++)
        sum+=v[i];
    return sum/v.size();
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

tuple<vector<vector<int>>,
      vector<string>,
      vector<vector<int>>,
      vector<string>> split_train_test (vector<vector<int>> &input_X,
                                         vector<string> &input_y,
                                         float f_testing)
{
    if(f_testing > 1.0)
    {
        cout << "f_testing cannot be higher than 1.0" << endl;
        exit(0);
    }
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    shuffle(begin(input_X), end(input_X), default_random_engine(seed));
    shuffle(begin(input_y), end(input_y), default_random_engine(seed));

    int lenght_X = input_X.size();
    int training_end = (int) ((1 - f_testing) * lenght_X);

    vector<vector<int>>::const_iterator first = input_X.begin();
    vector<vector<int>>::const_iterator mid = input_X.begin() + training_end;
    vector<vector<int>>::const_iterator last = input_X.begin() + lenght_X;

    vector<string>::const_iterator first_y = input_y.begin();
    vector<string>::const_iterator mid_y = input_y.begin() + training_end;
    vector<string>::const_iterator last_y = input_y.begin() + lenght_X;

    vector<vector<int>> X(first, mid);
    vector<vector<int>> testing_X(mid, last);
    vector<string> y(first_y, mid_y);
    vector<string> testing_y(mid_y, last_y);

    return make_tuple(X, y, testing_X, testing_y);
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

int experiment(vector<vector<int>> X,
               vector<string>y,
               int numBitsAddr,
               float confidenceThreshold,
               int numberOfRounds)
{
    // parameters:
    // WiSARD(int numBitsAddr,
	// 	      bool useBleaching=true,
    //        float confidenceThreshold=0.1,
    //        int defaultBleaching_b=1,
    //        bool randomizePositions=true,
    //        bool isCummulative=true,
    //        bool ignoreZeroAddr=false,
    //        int onlineMax = 2);

    vector<vector<int>> X_train;
    vector<string> y_train;
    vector<vector<int>> X_test;
    vector<string> y_test;

    for(int i = 0; i < numberOfRounds; i++)
    {
        //única diferença entre os dois modelos precisa ser o ignoreZeroAddr
        WiSARD * w1 = new WiSARD(numBitsAddr, true, confidenceThreshold, 1, true, true, false, 10);
        WiSARD * w2 = new WiSARD(numBitsAddr, true, confidenceThreshold, 1, true, true, true, 10);

        tie(X_train, y_train, X_test, y_test) = split_train_test(X,y,0.3);
        cout << X_train.size() << ";" << y_train.size() << ";";
        cout << X_test.size() << ";" << y_test.size() << endl;

        

        free(w1);
        free(w2);
    }
    return 0;
}


int main()
{
    string XFile = "data/imdb_cpp_X.csv";
    string yFile = "data/imdb_cpp_y.csv";
    vector<vector<int>> X;
    vector<string> y;
    tie(X, y) = loadData(XFile, yFile);
    experiment(X, y, 2, 0.1, 50);
}
