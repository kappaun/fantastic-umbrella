imdb:
	g++ Main.cpp -o teste1 -std=c++11 -lwann
	./teste1 data/imdb_cpp_X.csv data/imdb_cpp_y.csv result_imdb.csv
	rm teste1
	
sts:
	g++ Main.cpp -o teste2 -std=c++11 -lwann
	./teste2 data/new_sts_cpp_X.csv data/new_sts_cpp_y.csv result_sts.csv
	rm teste2

omd:
	g++ Main.cpp -o teste3 -std=c++11 -lwann
	./teste3 data/new_omd_cpp_X.csv data/new_omd_cpp_y.csv result_omd.csv
	rm teste3
