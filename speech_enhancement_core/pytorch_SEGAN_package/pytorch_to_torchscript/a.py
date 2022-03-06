import torch
from SEGAN.model import Generator


model_file = "G_5_0.3193.pkl"
#载入模型和训练参数
generator = Generator()
generator.load_state_dict(torch.load(model_file, map_location='cpu'))
#使用eval测试模式，不然会导致存在batchnorm模型无法使用
generator.eval()
#一个模型forward函数的随机输入（保证输入大小与训练时输入大小一致）
#torch.Size([1, 1, 16384])
#torch.Size([1, 1024, 8])
example = torch.rand(1, 1, 16384)
z = torch.rand(1, 1024, 8)
#  通过 tracing使用 torch.jit.trace 生成  torch.jit.ScriptModule.
traced_script_module = torch.jit.trace(generator, example_inputs=(example,z))
traced_script_module.save("./torch_script_eval.pt")


# output_size = torch.rand(1, 1, 16384)
# output = traced_script_module(output_size)
#
# # 测试输出
# print(output)

