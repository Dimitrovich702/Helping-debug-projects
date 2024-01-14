#include <iostream>
#include <string>
#include <unordered_map>

std::string encrypt(const std::string& input) {
    std::unordered_map<char, std::string> encryptionMap = {
        {'Q', "1"}, {'W', "2"}, {'E', "3"},{'R', "4"}, {'T', "5"}, {'Y', "6"}, {'U', "7"},{'I', "8"}, {'O', "9"}, {'P', "0"},
        {'A', "@"}, {'S', "#"}, {'D', "€"},{'F', "_"}, {'G', "&"}, {'H', "-"},{'J', "+"}, {'K', "("}, {'L', ")"},{'Ñ', "/"},
      {'Z', "*"}, {'X', "\""}, {'C', "\'"},{'V', ":"}, {'B', ";"}, {'N', "!"},{'M', "?"},{',', ","},{'.', "."},{' ', " "},
        {'1', "Q"}, {'2', "W"}, {'3', "E"},{'4', "R"}, {'5', "T"}, {'6', "Y"}, {'7', "U"},{'8', "I"}, {'9', "O"}, {'0', "P"},
       {'@', "A"}, {'#', "S"}, {'€', "D"},{'_', "F"}, {'&', "G"}, {'-', "H"},{'+', "J"}, {'(', "K"}, {')', "L"},{'/', "Ñ"},
        {'*', "Z"}, {'\"', "X"},
       {'\'', "C"},
        {':', "V"}, {';', "B"}, {'!', "N"},{'?', "M"}
     
        // characters here 
       // {'Q', "1"}, {'W', "2"},{'1', "Q"}, {'2', "W"}
    };

    std::string encryptedText;
    for (const char& c : input) {
        // check if in map
        if (encryptionMap.count(toupper(c)) > 0) {
            encryptedText += encryptionMap[toupper(c)];
        } else {
            // Keep stuff same if not in map
            encryptedText += c;
        }
    }

    return encryptedText;
}

int main() {
    std::string input;
    std::cout << " text to Algo: ";
    std::getline(std::cin, input);

    std::string encryptedText = encrypt(input);
    std::cout << "Algo text: " << encryptedText << std::endl;

    return 0;
} 
