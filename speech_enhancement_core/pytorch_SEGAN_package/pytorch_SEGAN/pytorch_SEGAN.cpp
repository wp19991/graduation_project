// pytorch_SEGAN.cpp: 定义应用程序的入口点。
//

#include <torch/script.h> // One-stop header.
#include <torch/csrc/autograd/variable.h>
#include <vector>
#include <iostream>
#include <memory>
#include <fstream>

int main()
{
	
    // Deserialize the ScriptModule from a file using torch::jit::load().
    torch::jit::script::Module module;
    module = torch::jit::load("C:/pt/torch_script_eval.pt");

    //assert(module != nullptr);
    std::cout << "ok\n";
    std::ifstream  fin;
    std::ofstream fout;
    fin.open("./wav/w_0", std::ios::in);
    int buf[1024] = { 0 };
    while (fin >> buf)
    {
        std::cout << buf << std::endl;//每一次的buf是空格或回车键（即白色字符）分开的元素
    }

 // Create a vector of inputs.
 //std::vector<torch::jit::IValue> inputs;
 //inputs.push_back(torch::ones({ 1, 3, 224, 224 }));
//
//    // Execute the model and turn its output into a tensor.
//    at::Tensor output = module->forward(inputs).toTensor();
//
//    std::cout << output.slice(/*dim=*/1, /*start=*/0, /*end=*/5) << '\n';
//    while (1);



	return 0;
}
