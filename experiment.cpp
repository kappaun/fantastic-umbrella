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

double stdeviation = 0.0;
double meantime = 0.0;
double meantimepredict = 0.0;

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

double deviation(vector<double> v, double ave)
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
extern "C" double testing(int numBitsAddr, float confidenceThreshold, int zero)
{

    int numberOfRounds = 100;

    vector<vector<int>> X;
    vector<string> y;
    vector<string> y_pred;

    vector<vector<int>> X_test;
    vector<string> y_test;
    vector<vector<int>> X_train;
    vector<string> y_train;

    string XFile = "temp_data/X_test";
    string yFile = "temp_data/y_test";

    tie(X, y) = loadData(XFile, yFile);
    // tie(X_test, y_test) = loadData(XtestFile, ytestFile);


    double accuracy;
    vector<double> accuracies;

    int ignoreZeroAddr = false;

    if(zero)
    {
        cout << "ignoreZeroAddr = 1" << endl;
        ignoreZeroAddr = true;
    }
    else
    {
        cout << "ignoreZeroAddr = 0" << endl;
        ignoreZeroAddr = false;
    }

    for(int i = 0; i < numberOfRounds; i++)
    {
        // cout << "iter: " << i << endl;
        // tie(X_train, y_train, X_test, y_test) = split_train_test(X,y,0.3);
        auto begin = std::chrono::high_resolution_clock::now();

        WiSARD * w = new WiSARD(numBitsAddr, true, confidenceThreshold, 1, true, true, ignoreZeroAddr, 10);
        
        auto end = std::chrono::high_resolution_clock::now();

        meantime += std::chrono::duration_cast<std::chrono::nanoseconds>(end-begin).count();

        tie(X_train, y_train, X_test, y_test) = split_train_test(X,y,0.05);
        w->fit(X_train, y_train);

        auto begin2 = std::chrono::high_resolution_clock::now();

        y_pred = w->predict(X_test);

        auto end2 = std::chrono::high_resolution_clock::now();

        meantimepredict += std::chrono::duration_cast<std::chrono::nanoseconds>(end2-begin2).count();

        accuracy = accuracyScore(y_test, y_pred);
        // cout << "acc: " << accuracy << endl;
        accuracies.push_back(accuracy);
        free(w);
    }
    double avg = accumulate(accuracies.begin(), accuracies.end(), 0.0)/accuracies.size();

    stdeviation = deviation(accuracies, avg);
    cout << "avg: " << avg << endl;
    cout << "std: " << deviation(accuracies, avg) << endl;
    return avg;
}
extern "C" double getdev()
{
    return stdeviation;
}

extern "C" double gettime()
{
    return meantime/100;
}

extern "C" double gettimepredict()
{
    return meantimepredict/100;
}

extern "C" double object_function(int numBitsAddr, float confidenceThreshold)
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

    int numberOfRounds = 10;
    vector<vector<int>> X;
    vector<string> y;

    string XFile = "temp_data/X_train";
    string yFile= "temp_data/y_train";

    tie(X, y) = loadData(XFile, yFile);

    vector<vector<int>> X_train;
    vector<string> y_train;
    vector<vector<int>> X_test;
    vector<string> y_test;

    vector<string> y_pred;

    double accuracy;
    vector<double> accuracies;
    cout << "initiating system..." << endl;
    
    for(int i = 0; i < numberOfRounds; i++)
    {
        cout << "iter: " << i << endl;
        tie(X_train, y_train, X_test, y_test) = split_train_test(X,y,0.3);
        WiSARD * w = new WiSARD(numBitsAddr, true, confidenceThreshold, 1, true, true, true, 10);
        
            

        w->fit(X_train, y_train);
        y_pred = w->predict(X_test);
        accuracy = accuracyScore(y_test, y_pred);
        accuracies.push_back(accuracy);
        free(w);
    }

    return accumulate( accuracies.begin(), accuracies.end(), 0.0)/accuracies.size();
}

int main(int argc, char** argv)
{

    /*Argumentos de entrada da main devem ser:
        >> arquivo de entrada X
        >> arquivo de entrada y
        >> arquivo de saida (ainda preciso decidir o formato)
    */
    // std::cout << argv[1] << '\n';
    // std::cout << argv[2] << '\n';
    // std::cout << "confidence: " << argv[3] << '\n';
    // std::cout << "number of bits:" << argv[4] << '\n';

    // ofstream output;
    // // output.open(argv[3]);

    // string XFile = argv[1];
    // string yFile = argv[2];

    // float confidenceThreshold = stof(argv[3]);
    // int numBits = stoi(argv[4]);

    // vector<vector<int>> X;
    // vector<string> y;

    // tie(X, y) = loadData(XFile, yFile);

    // // unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    // // shuffle(begin(X), end(X), default_random_engine(seed));
    // // shuffle(begin(y), end(y), default_random_engine(seed));


    // // std::vector<string> y_test = std::vector<string>(y.begin() + int(y.size()*0.7), y.end());
    // // std::vector<string> y_train = std::vector<string>(y.begin(), y.end() - int(y.size()*0.3));

    // // std::vector<string> X_test = std::vector<string>(X.begin() + int(X.size()*0.7), X.end());
    // // std::vector<string> X_train = std::vector<string>(X.begin(), X.end() - int(X.size()*0.3));

    // cout << experiment(X, y, numBits, confidenceThreshold, 2) << endl;

    return 0;

}
