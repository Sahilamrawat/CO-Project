#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>

std::map<std::string, std::vector<int>> R_TYPE_INSTRUCTIONS = {{"add", {0b0000000, 0b000, 0b0110011}}, {"sub", {0b0100000, 0b000, 0b0110011}}, {"sll", {0b0000000, 0b001, 0b0110011}}};
std::map<std::string, std::vector<int>> I_TYPE_INSTRUCTIONS = {{"addi", {0b000, 0b0010011}}};
std::map<std::string, std::vector<int>> S_TYPE_INSTRUCTIONS = {{"sw", {0b010, 0b0100011}}};
std::map<std::string, std::vector<int>> B_TYPE_INSTRUCTIONS = {{"beq", {0b000, 0b1100011}}};
std::map<std::string, int> U_TYPE_INSTRUCTIONS = {{"lui", 0b0110111}};
std::map<std::string, int> J_TYPE_INSTRUCTIONS = {{"jal", 0b1101111}};

int r_type_encoding(int rd, int rs1, int rs2, std::string instruction) {
    if (R_TYPE_INSTRUCTIONS.find(instruction) == R_TYPE_INSTRUCTIONS.end()) {
        throw std::invalid_argument("Invalid R-type instruction: " + instruction);
    }
    int funct7 = R_TYPE_INSTRUCTIONS[instruction][0];
    int funct3 = R_TYPE_INSTRUCTIONS[instruction][1];
    int opcode = R_TYPE_INSTRUCTIONS[instruction][2];
    int binary = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode;
    return binary;
}
?><
int i_type_encoding(int rd, int rs1, int imm, std::string instruction) {
    if (I_TYPE_INSTRUCTIONS.find(instruction) == I_TYPE_INSTRUCTIONS.end()) {   
        throw std::invalid_argument("Invalid I-type instruction: " + instruction);
    }
    int funct3 = I_TYPE_INSTRUCTIONS[instruction][0];
    int opcode = I_TYPE_INSTRUCTIONS[instruction][1];
    int binary = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode;
    return binary;
}

int s_type_encoding(int rs1, int rs2, int imm, std::string instruction) {
    if (S_TYPE_INSTRUCTIONS.find(instruction) == S_TYPE_INSTRUCTIONS.end()) {
        throw std::invalid_argument("Invalid S-type instruction: " + instruction);
    }
    int funct3 = S_TYPE_INSTRUCTIONS[instruction][0];
    int opcode = S_TYPE_INSTRUCTIONS[instruction][1];
    int binary = (imm << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | opcode;
    return binary;
}

int b_type_encoding(int rs1, int rs2, int imm, std::string instruction) {
    if (B_TYPE_INSTRUCTIONS.find(instruction) == B_TYPE_INSTRUCTIONS.end()) {
        throw std::invalid_argument("Invalid B-type instruction: " + instruction);
    }
    int funct3 = B_TYPE_INSTRUCTIONS[instruction][0];
    int opcode = B_TYPE_INSTRUCTIONS[instruction][1];
    int binary = (imm << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | opcode;
    return binary;
}

int u_type_encoding(int rd, int imm, std::string instruction) {
    if (U_TYPE_INSTRUCTIONS.find(instruction) == U_TYPE_INSTRUCTIONS.end()) {
        throw std::invalid_argument("Invalid U-type instruction: " + instruction);
    }
    int opcode = U_TYPE_INSTRUCTIONS[instruction];
    int binary = (imm << 12) | (rd << 7) | opcode;
    return binary;
}

int j_type_encoding(int rd, int imm, std::string instruction) {
    if (J_TYPE_INSTRUCTIONS.find(instruction) == J_TYPE_INSTRUCTIONS.end()) {
        throw std::invalid_argument("Invalid J-type instruction: " + instruction);
    }
    int opcode = J_TYPE_INSTRUCTIONS[instruction];
    int binary = (imm << 20) | (rd << 7) | opcode;
    return binary;
}

std::vector<int> assemble(std::string assembly_file) {
    std::ifstream file(assembly_file);
    std::string line;
    std::vector<int> binary_output;

    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') {
            continue;
        }

        std::string instruction;
        std::vector<int> tokens;
        std::istringstream iss(line);
        iss >> instruction;
        int token;
        while (iss >> token) {
            tokens.push_back(token);
        }

        int binary;
        if (R_TYPE_INSTRUCTIONS.count(instruction)) {
            binary = r_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
        } else if (I_TYPE_INSTRUCTIONS.count(instruction)) {
            binary = i_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
        } else if (S_TYPE_INSTRUCTIONS.count(instruction)) {
            binary = s_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
        } else if (B_TYPE_INSTRUCTIONS.count(instruction)) {
            binary = b_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
        } else if (U_TYPE_INSTRUCTIONS.count(instruction)) {
            binary = u_type_encoding(tokens[0], tokens[1], instruction);
        } else if (J_TYPE_INSTRUCTIONS.count(instruction)) {
            binary = j_type_encoding(tokens[0], tokens[1], instruction);
        } else {
            std::cout << "Error: Unknown instruction '" << instruction << "'" << std::endl;
            continue;
        }

        binary_output.push_back(binary);
    }

    return binary_output;
}

std::vector<int> binary_output = assemble("example.s");

std::ofstream output_file("output.txt");
for (int binary : binary_output) {
    output_file << binary << std::endl;
}
output_file.close();

return 0;
