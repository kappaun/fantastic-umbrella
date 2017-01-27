run:
	g++ Main.cpp -o teste -std=c++11 -lwann
	./teste data/new_omd_cpp_X.csv data/new_omd_cpp_y.csv result_new_omd.csv
	rm teste
