import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from llm_module import LLMAgent
import torch
from point_e.diffusion.configs import DIFFUSION_CONFIGS, diffusion_from_config
from point_e.diffusion.sampler import PointCloudSampler
from point_e.models.download import load_checkpoint
from point_e.models.configs import MODEL_CONFIGS, model_from_config
from point_e.util.pc_to_mesh import marching_cubes_mesh
from tqdm.auto import tqdm
import time

class InteractiveSystem:
    """多模态交互系统"""
    def __init__(self, api_key: str):
        self.llm_agent = LLMAgent(api_key)
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

        # 初始化t2p
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print('creating base model...')
        base_name = 'base40M-textvec'
        self.base_model = model_from_config(MODEL_CONFIGS[base_name], self.device)
        self.base_model.eval()
        self.base_diffusion = diffusion_from_config(DIFFUSION_CONFIGS[base_name])

        print('creating upsample model...')
        self.upsampler_model = model_from_config(MODEL_CONFIGS['upsample'], self.device)
        self.upsampler_model.eval()
        self.upsampler_diffusion = diffusion_from_config(DIFFUSION_CONFIGS['upsample'])

        print('downloading base checkpoint...')
        self.base_model.load_state_dict(load_checkpoint(base_name, self.device))

        print('downloading upsampler checkpoint...')
        self.upsampler_model.load_state_dict(load_checkpoint('upsample', self.device))

        self.sampler = PointCloudSampler(
            device=self.device,
            models=[self.base_model, self.upsampler_model],
            diffusions=[self.base_diffusion, self.upsampler_diffusion],
            num_points=[1024, 4096 - 1024],
            aux_channels=['R', 'G', 'B'],
            guidance_scale=[3.0, 0.0],
            model_kwargs_key_filter=('texts', ''),  # Do not condition the upsampler at all
        )

        # 初始化p2m
        print('creating SDF model...')
        name = 'sdf'
        self.sdf_model = model_from_config(MODEL_CONFIGS[name], self.device)
        self.sdf_model.eval()

        print('loading SDF model...')
        self.sdf_model.load_state_dict(load_checkpoint(name, self.device))

    def process_user_request(self, user_input: str, temperature: float = 0.7) -> str:
        """处理用户请求"""
        # 1. LLM生成3D提示
        structured_params = self.llm_agent.process_user_query(user_input, temperature)
        prompt = f"{structured_params['object']} {structured_params['color']} {structured_params['material']} {structured_params['style']}"
        prompt = prompt.strip()
        print(prompt)

        # 2. 生成3D点云
        samples = None
        for x in tqdm(self.sampler.sample_batch_progressive(batch_size=1, model_kwargs=dict(texts=[prompt]))):
            samples = x
        pc = self.sampler.output_to_point_clouds(samples)[0]

        # 3. 点云转mesh
        mesh = marching_cubes_mesh(
            pc=pc,
            model=self.sdf_model,
            batch_size=4096,
            grid_size=128, 
            progress=True,
        )

        # 4. 保存mesh，使用时间戳作为文件名的一部分
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = os.path.join(self.output_dir, f"mesh_{timestamp}.ply")
        with open(output_path, 'wb') as f:
            mesh.write_ply(f)

        return f"模型生成完成，保存路径: {output_path}"


class GUISystem:
    """图形界面"""
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("3D模型生成")
        self.root.geometry("800x700")
        self.interactive_system = InteractiveSystem(api_key)
        self.create_widgets()

    def create_widgets(self):
        # 标题与说明
        tk.Label(self.root, text="3D模型生成", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text="支持文本描述生成3D模型", font=("Arial", 10)).pack(pady=5)

        # 文本输入区
        tk.Label(self.root, text="输入模型描述 (如: 绿色的椅子)").pack(pady=5)
        self.prompt_entry = scrolledtext.ScrolledText(self.root, height=4)
        self.prompt_entry.pack(fill=tk.BOTH, padx=10, pady=5)

        # 参数控制区
        param_frame = tk.Frame(self.root)
        param_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(param_frame, text="Temperature:").pack(side=tk.LEFT, padx=5)
        self.temp_entry = tk.Entry(param_frame, width=10)
        self.temp_entry.insert(0, "0.7")
        self.temp_entry.pack(side=tk.LEFT, padx=5)

        # 功能按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="文本生成3D模型",
                  command=lambda: self.generate_model(),
                  width=18).pack(side=tk.LEFT, padx=10)

        # 结果显示区
        tk.Label(self.root, text="生成结果", font=("Arial", 12)).pack(pady=5)
        self.result_text = scrolledtext.ScrolledText(self.root, height=8)
        self.result_text.pack(fill=tk.BOTH, padx=10, pady=5)

        # 日志显示区
        tk.Label(self.root, text="处理日志", font=("Arial", 12)).pack(pady=5)
        self.log_text = scrolledtext.ScrolledText(self.root, height=10)
        self.log_text.pack(fill=tk.BOTH, padx=10, pady=5)

    def generate_model(self):
        prompt = self.prompt_entry.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showerror("错误", "请输入模型描述")
            return

        try:
            temperature = float(self.temp_entry.get())

            self.log_text.insert(tk.END, f"开始生成（文本输入）: {prompt}\n")
            self.log_text.see(tk.END)

            # 异步处理
            threading.Thread(
                target=self._generate_thread,
                args=(prompt, temperature)
            ).start()
        except ValueError:
            messagebox.showerror("错误", "Temperature需为数字")

    def _generate_thread(self, prompt, temperature):
        result = self.interactive_system.process_user_request(prompt, temperature)

        # 更新UI
        self.root.after(0, lambda: self.result_text.insert(tk.END, f"{result}\n"))
        self.root.after(0, lambda: self.log_text.insert(tk.END, f"生成完成: {time.strftime('%H:%M:%S')}\n"))
        self.root.after(0, lambda: self.result_text.see(tk.END))
        self.root.after(0, lambda: self.log_text.see(tk.END))


if __name__ == "__main__":
    # 从环境变量中获取 API 密钥
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("请设置 API_KEY 环境变量")

    # 启动GUI
    root = tk.Tk()
    app = GUISystem(root, api_key)
    root.mainloop() 