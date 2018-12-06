#include <iostream>
#include <string>
#include <vector>

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
	if(input[0] == '\"' && input[input.size()-1] == '\"') {
		errorCode = 0;
		return input.substr(1, input.size()-2);
	}
	errorCode = 1;
	return "";
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
  splits.push_back(input.substr(lastIndex, input.size() - lastIndex));
}

/** Converts a string to an array of strings. */
std::vector<std::string> stoa(std::string input, int& errorCode, std::vector<std::string> &arr) {
	if(input[0] == '[' && input[input.size()-1] == ']') {
		input = input.substr(1, input.size()-2);
		errorCode = 0;
		splitString(arr, input, ", ");
		std::cout << "Size: " << arr.size() << std::endl;
		int stosErrorCode = 0;
		for(size_t i = 0; i < arr.size(); i++) {
			arr[i] = stos(arr[i], stosErrorCode);
			if(stosErrorCode != 0) {
				break;
			}
		}
		return arr;
	}
	errorCode = 1;
	return arr;
}

int main() {
	std::string input = "[\"../testimages/onetarget.jpg\", \"../testimages/faketargets.png\", \"/home/pi/src/calibration/green_60cm_20deg\", \"/home/pi/src/calibration/green_90cm_20deg\", \"/home/pi/src/calibration/green_120cm_20deg\", \"/home/pi/src/calibration/green_60cm_10deg\", \"/home/pi/src/calibration/green_90cm_10deg\", \"/home/pi/src/calibration/green_120cm_10deg\", \"../waamv/orig0.jpg\", \"../waamv/orig1.jpg\", \"../waamv/orig2.jpg\", \"../waamv/orig3.jpg\", \"../waamv/orig4.jpg\"]";
	std::vector<std::string> testVector;
	int errorCode = 0;
	//splitString(testVector, input, ", ");
	testVector = stoa(input, errorCode, testVector);
	std::cout << "Error code: " << errorCode << std::endl;
	std::cout << "Size: " << testVector.size() << std::endl;
	for(size_t i = 0; i < testVector.size(); i++) {
		std::cout << testVector[i] << std::endl;
	}
	do {
		std::cout << "Enter input: \n";
		getline (std::cin, input);
		std::cout << getType(input) << "\n";
	} while(input!= "");
}
