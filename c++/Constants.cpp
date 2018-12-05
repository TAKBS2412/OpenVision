#include <iostream>
#include <string>

std::string getType(std::string input) {
    if('0' <= input[0] && input[0] <= '9') {
        for(std::string ::size_type i = 0; i < input.size(); i++) {
            if(input[i] == '.') {
                return "Double";
            }
        }
        return "Integer";
    }
    switch(input[0]) {
        case '\"':
            return "String";
        case '[':
            return "Array";
        case 'T':
        case 'F':
            return "Boolean";
        default:
            return "Invalid type";
    }
}

/** Splits up the string input using the delimiter delim, and stores the resulting substring in the vector splits. */
void splitString(std::vector<std::string> &splits, std::string input, std::string delim) {
  size_t lastIndex = 0; // This will either be 0 or the index of the last character of delim.
  for(size_t i = 0; i < input.size() - delim.size() + 1; i++) {
    if(input.substr(i, delim.size()) == delim) {
      splits.push_back(input.substr(lastIndex, i - lastIndex));
      lastIndex = i + delim.size();
    }
  }
}

std::string stos(std::string input, int& errorCode) {
	if(input[0] == '\"' && input[input.size()-1] == '\"') {
		errorCode = 0;
		return input.substr(1, input.size()-2);
	}
	errorCode = 1;
	return "";
}

int main() {
	std::string input = "";
	do {
		std::cout << "Enter input: \n";
		getline (std::cin, input);
		std::cout << getType(input) << "\n";
	} while(input!= "");
}
