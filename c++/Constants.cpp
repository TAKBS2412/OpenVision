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

std::string stos(std::string input, int& errorCode) {
	// Assume that the first character is a double quotation mark " because we've already checked.
	if(input[input.size()-1] == '\"') {
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
