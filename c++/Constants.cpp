#include <iostream>
#include <string>

int main() {
	std::string input = "";
	do {
		std::cout << "Enter input: \n";
		getline (std::cin, input);
		std::cout << input << "\n";
	} while(input!= "");
}
