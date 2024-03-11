#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <stdexcept>
#include <cstdlib>

// Define the opcode values for each instruction type
const int R_TYPE_OPCODE = 0b0110011;
const int I_TYPE_OPCODE = 0b0010011;
const int S_TYPE_OPCODE = 0b0100011;
const int B_TYPE_OPCODE = 0b1100011;
const int U_TYPE_OPCODE = 0b0110111;
const int J_TYPE_OPCODE = 0b1101111;

// Define the funct3 values for specific R and I type instructions
const int ADD_FUNCT3 = 0b000;
const int SUB_FUNCT3 = 0b000;
const int SLT_FUNCT3 = 0b010;
const int SLTU_FUNCT3 = 0b011;
const int XOR_FUNCT3 = 0b100;
const int SLL_FUNCT3 = 0b001;
const int SRL_FUNCT3 = 0b101;
const int OR_FUNCT3 = 0b110;
const int AND_FUNCT3 = 0b111;

const int LB_FUNCT3 = 0b000;
const int LH_FUNCT3 = 0b001;
const int LW_FUNCT3 = 0b010;
const int LD_FUNCT3 = 0b011;
const int ADDI_FUNCT3 = 0b000;
const int SLTIU_FUNCT3 = 0b011;
const int JALR_FUNCT3 = 0b000;

const int SB_FUNCT3 = 0b000;
const int SH_FUNCT3 = 0b001;
const int SW_FUNCT3 = 0b010;
const int SD_FUNCT3 = 0b011;

const int BEQ_FUNCT3 = 0b000;
const int BNE_FUNCT3 = 0b001;
const int BGE_FUNCT3 = 0b101;
const int BGEU_FUNCT3 = 0b111;
const int BLT_FUNCT3 = 0b100;
const int BLTU_FUNCT3 = 0b110;

const int LUI_OPCODE = 0b0110111;
const int AUIPC_OPCODE = 0b0010111;

const int JAL_OPCODE = 0b1101111;

std::map<std::string, std::vector<int>> R_TYPE_FUNCTIONS = {
    {"add", {ADD_FUNCT3, R_TYPE_OPCODE}},
    {"sub", {SUB_FUNCT3, R_TYPE_OPCODE}},
    {"slt", {SLT_FUNCT3, R_TYPE_OPCODE}},
    {"sltu", {SLTU_FUNCT3, R_TYPE_OPCODE}},
    {"xor", {XOR_FUNCT3, R_TYPE_OPCODE}},
    {"sll", {SLL_FUNCT3, R_TYPE_OPCODE}},
    {"srl", {SRL_FUNCT3, R_TYPE_OPCODE}},
    {"or", {OR_FUNCT3, R_TYPE_OPCODE}},
    {"and", {AND_FUNCT3, R_TYPE_OPCODE}},
};

std::map<std::string, std::vector<int>> I_TYPE_FUNCTIONS = {
    {"lb", {LB_FUNCT3, I_TYPE_OPCODE}},
    {"lh", {LH_FUNCT3, I_TYPE_OPCODE}},
    {"lw", {LW_FUNCT3, I_TYPE_OPCODE}},
    {"ld", {LD_FUNCT3, I_TYPE_OPCODE}},
    {"addi", {ADDI_FUNCT3, I_TYPE_OPCODE}},
    {"sltiu", {SLTIU_FUNCT3, I_TYPE_OPCODE}},
    {"jalr", {JALR_FUNCT3, I_TYPE_OPCODE}},
};

std::map<std::string, std::vector<int>> S_TYPE_FUNCTIONS = {
    {"sb", {SB_FUNCT3, S_TYPE_OPCODE}},
    {"sh", {SH_FUNCT3, S_TYPE_OPCODE}},
    {"sw", {SW_FUNCT3, S_TYPE_OPCODE}},
    {"sd", {SD_FUNCT3, S_TYPE_OPCODE}},
};

std::map<std::string, std::vector<int>> B_TYPE_FUNCTIONS = {
    {"beq", {BEQ_FUNCT3, B_TYPE_OPCODE}},
    {"bne", {BNE_FUNCT3, B_TYPE_OPCODE}},
    {"bge", {BGE_FUNCT3, B_TYPE_OPCODE}},
    {"bgeu", {BGEU_FUNCT3, B_TYPE_OPCODE}},
    {"blt", {BLT_FUNCT3, B_TYPE_OPCODE}},
    {"bltu", {BLTU_FUNCT3, B_TYPE_OPCODE}},
};

std::map<std::string, int> U_TYPE_FUNCTIONS = {
    {"lui", LUI_OPCODE},
    {"auipc", AUIPC_OPCODE},
};

std::map<std::string, int> J_TYPE_FUNCTIONS = {
    {"jal", JAL_OPCODE},
};

// Define a common encoding function for R, I, S, B, U, J types
int common_encoding(int opcode, int rd, int rs1, int funct3, int rs2, int funct7 = 0) {
    return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode;
}

std::string int_to_bin(int num, int padding = 0) {
    std::string result;
    while (num) {
        result.insert(result.begin(), '0' + (num & 1));
        num >>= 1;
    }
    while (result.size() < padding) {
        result.insert(result.begin(), '0');
    }
    return result.empty() ? "0" : result;
}

void write_binary_to_file(const std::string& file_path, const std::vector<int>& binary_output) {
    std::ofstream output_file(file_path);
    if (!output_file.is_open()) {
        throw std::runtime_error("Failed to open the output file.");
    }

    for (int binary : binary_output) {
        output_file << int_to_bin(binary, 32) << std::endl;
    }

    output_file.close();
}

int r_type_encoding(int rd, int rs1, int rs2, const std::string& instruction) {
    if (R_TYPE_FUNCTIONS.find(instruction) == R_TYPE_FUNCTIONS.end()) {
        throw std::invalid_argument("Invalid R-type instruction: " + instruction);
    }
    int funct3 = R_TYPE_FUNCTIONS[instruction][0];
    int opcode = R_TYPE_FUNCTIONS[instruction][1];
    int funct7 = 0;  // Default funct7 value for most R-type instructions
    return common_encoding(opcode, rd, rs1, funct3, rs2, funct7);
}

int i_type_encoding(int rd, int rs1, int imm, const std::string& instruction) {
    if (I_TYPE_FUNCTIONS.find(instruction) == I_TYPE_FUNCTIONS.end()) {
        throw std::invalid_argument("Invalid I-type instruction: " + instruction);
    }
    int funct3 = I_TYPE_FUNCTIONS[instruction][0];
    int opcode = I_TYPE_FUNCTIONS[instruction][1];
    return common_encoding(opcode, rd, rs1, funct3, imm);
}

int s_type_encoding(int rd, int rs1, int imm, const std::string& instruction) {
    if (S_TYPE_FUNCTIONS.find(instruction) == S_TYPE_FUNCTIONS.end()) {
        throw std::invalid_argument("Invalid S-type instruction: " + instruction);
    }
    int funct3 = S_TYPE_FUNCTIONS[instruction][0];
    int opcode = S_TYPE_FUNCTIONS[instruction][1];
    return common_encoding(opcode, rd, rs1, funct3, imm);
}

int b_type_encoding(int rs1, int rs2, int imm, const std::string& instruction) {
    if (B_TYPE_FUNCTIONS.find(instruction) == B_TYPE_FUNCTIONS.end()) {
        throw std::invalid_argument("Invalid B-type instruction: " + instruction);
    }
    int funct3 = B_TYPE_FUNCTIONS[instruction][0];
    int opcode = B_TYPE_FUNCTIONS[instruction][1];
    return common_encoding(opcode, 0, rs1, funct3, rs2, imm);
}

int u_type_encoding(int rd, int imm, const std::string& instruction) {
    if (U_TYPE_FUNCTIONS.find(instruction) == U_TYPE_FUNCTIONS.end()) {
        throw std::invalid_argument("Invalid U-type instruction: " + instruction);
    }
    int opcode = U_TYPE_FUNCTIONS[instruction];
    return common_encoding(opcode, rd, 0, 0, 0, imm);
}

int j_type_encoding(int rd, int imm, const std::string& instruction) {
    if (J_TYPE_FUNCTIONS.find(instruction) == J_TYPE_FUNCTIONS.end()) {
        throw std::invalid_argument("Invalid J-type instruction: " + instruction);
    }
    int opcode = J_TYPE_FUNCTIONS[instruction];
    return common_encoding(opcode, rd, 0, 0, 0, imm);
}

std::vector<int> assemble(const std::string& assembly_file) {
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
        try {
            if (R_TYPE_FUNCTIONS.count(instruction)) {
                binary = r_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
            } else if (I_TYPE_FUNCTIONS.count(instruction)) {
                binary = i_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
            } else if (S_TYPE_FUNCTIONS.count(instruction)) {
                binary = s_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
            } else if (B_TYPE_FUNCTIONS.count(instruction)) {
                binary = b_type_encoding(tokens[0], tokens[1], tokens[2], instruction);
            } else if (U_TYPE_FUNCTIONS.count(instruction)) {
                binary = u_type_encoding(tokens[0], tokens[1], instruction);
            } else if (J_TYPE_FUNCTIONS.count(instruction)) {
                binary = j_type_encoding(tokens[0], tokens[1], instruction);
            } else {
                std::cout << "Error: Unknown instruction '" << instruction << "'" << std::endl;
                continue;
            }

            binary_output.push_back(binary);
        } catch (const std::invalid_argument& e) {
            std::cerr << "Error: " << e.what() << std::endl;
        }
    }

    return binary_output;
}


int main() {
    std::vector<int> binary_output = assemble("C:\\Users\\kumar\\Downloads\\test3.asm");

    write_binary_to_file("C:\\Users\\kumar\\Downloads\\TEst.txt", binary_output);

    // Open the output file
    std::string command = "notepad C:\\Users\\kumar\\Downloads\\TEst.txt";  // Change 'notepad' to your preferred text editor
    system(command.c_str());

    return 0;
}