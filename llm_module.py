import openai
import json
import re
from typing import Dict, Any
from openai import OpenAI
import time

class LLMAgent:
    def __init__(self, api_key: str, model_name: str = "deepseek-ai/DeepSeek-V3"):
        """初始化LLM代理，处理中英文输入并输出英文结构化JSON"""
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.siliconflow.cn/" 
        )
        self.model = model_name  
        self.conversation_history = []
        
        # 指令注入防护配置
        self.dangerous_patterns = [
            r'system:', r'user:', r'assistant:',  # 基础角色标签
            r'```json', r'```',                  # 代码块标识
            r'\{.*\}',                           # JSON格式
            r'http[s]?://\S+',                   # URL链接
        ]
        self.dangerous_regex = re.compile(
            '|'.join(self.dangerous_patterns), 
            re.IGNORECASE | re.DOTALL
        )

        # 中英文系统提示词
        self.system_prompt_en = """
        You are a professional 3D model generation assistant. Convert the user's request into a JSON format with English fields and values. Required fields:
        - object: Main object (e.g., "chair")
        - dimensions: Size (e.g., "45cm x 45cm x 85cm")
        - material: Material (e.g., "wood")
        - color: Color (e.g., "green")
        - style: Design style (e.g., "modern")
        - modifications: Additional features (array of strings)

        Ensure all values are English strings. Output valid JSON only, no extra text.
        """

        self.system_prompt_zh = """
        你是一个专业的3D模型生成助手。请将用户的需求转换为JSON格式，包含以下字段：
        - object: 必需，描述要生成的主要物体（如"椅子"）
        - dimensions: 可选，物体尺寸（如"45cm x 45cm x 85cm"）
        - material: 可选，材质（如"木质"）
        - color: 可选，颜色（如"绿色"）
        - style: 可选，设计风格（如"现代风格"）
        - modifications: 可选，其他修改或功能描述

        确保所有字段的值都是英文。输出必须是格式正确的JSON，不包含任何额外文本。
        """

    def _sanitize_input(self, text: str) -> str:
        """清理用户输入，防止指令注入"""
        if not text:
            return text
            
        # 移除潜在的危险模式
        sanitized_text = self.dangerous_regex.sub('[FILTERED]', text)
        
        # 规范化输入：去除多余空格和换行
        sanitized_text = re.sub(r'\s+', ' ', sanitized_text).strip()
        
        return sanitized_text

    def generate_3d_prompt(self, text: str, temperature: float = 0.2) -> dict[str, any]:
        sanitized_text = self._sanitize_input(text)
        if self._detect_language(sanitized_text) == "zh":
            system_prompt = self.system_prompt_zh
            user_prompt = f"""将以下中文描述转换为英文JSON："{sanitized_text}" """
        else:
            system_prompt = self.system_prompt_en
            user_prompt = f"""Convert the following description to English JSON: "{sanitized_text}" """

        max_retries = 5
        base_delay = 1  # 初始延迟时间（秒）
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=500
                )
                json_text = self._extract_json_from_text(response.choices[0].message.content)
                parsed_data = self._parse_and_validate(json_text)

                parsed_data["object"] = self._ensure_english(parsed_data["object"])
                parsed_data["material"] = self._ensure_english(parsed_data["material"])
                parsed_data["style"] = self._ensure_english(parsed_data["style"])

                return parsed_data

            except openai.RateLimitError as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed after {max_retries} attempts: {e}")
                    return self._fallback_generation(sanitized_text)
            except Exception as e:
                print(f"LLM处理失败: {e}")
                return self._fallback_generation(sanitized_text)
 
    def process_user_query(self, user_input: str, temperature: float = 0.7) -> Dict[str, Any]:
        structured_params = self.generate_3d_prompt(user_input, temperature)
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({
            "role": "assistant",
            "content": json.dumps(structured_params, ensure_ascii=False)
        })
        return structured_params

    def _detect_language(self, text: str) -> str:
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        total_chars = len(text)
        return "zh" if chinese_chars / total_chars > 0.3 else "en"

    def _extract_json_from_text(self, text: str) -> str:
        match = re.search(r'```json?\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        match = re.search(r'({.*?})', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def _parse_and_validate(self, json_text: str) -> Dict[str, Any]:
        try:
            data = json.loads(json_text)
            normalized = {
                "object": data.get("object", data.get("物体", "object")),
                "dimensions": data.get("dimensions", data.get("尺寸", "")),
                "material": data.get("material", data.get("材质", "")),
                "color": data.get("color", data.get("颜色", "")),
                "style": data.get("style", data.get("风格", "")),
                "modifications": data.get("modifications", data.get("修改", []))
            }
            return normalized
        except:
            return self._fallback_generation(json_text)

    def _ensure_english(self, text: str) -> str:
        translations = {
            "椅子": "chair", "桌子": "table", "沙发": "sofa", "床": "bed",
            "台灯": "lamp", "书架": "bookshelf", "花瓶": "vase", "雕塑": "sculpture",
            "木质": "wooden", "金属": "metal", "塑料": "plastic", "玻璃": "glass",
            "红色": "red", "绿色": "green", "蓝色": "blue", "黄色": "yellow",
            "现代风格": "modern", "复古风格": "vintage", "工业风格": "industrial",
            "简约风格": "minimalist", "豪华风格": "luxury"
        }
        if all('\u4e00' <= char <= '\u9fff' for char in text.strip() if char.strip()):
            return translations.get(text, "object")
        if re.search(r'[a-zA-Z]', text):
            return text
        return "object"

    def _fallback_generation(self, text: str) -> Dict[str, Any]:
        obj = self._ensure_english(self._infer_object_from_prompt(text))
        return {
            "object": obj,
            "dimensions": "",
            "material": "",
            "color": "",
            "style": "",
            "modifications": []
        }

    def _infer_object_from_prompt(self, prompt: str) -> str:
        objects = {
            "chair": ["chair", "椅子"],
            "table": ["table", "桌子"],
            "sofa": ["sofa", "沙发"],
            "bed": ["bed", "床"],
            "lamp": ["lamp", "台灯"],
            "bookshelf": ["bookshelf", "书架"],
            "vase": ["vase", "花瓶"],
            "sculpture": ["sculpture", "雕塑"]
        }
        for obj, keywords in objects.items():
            for keyword in keywords[:1]:
                if keyword.lower() in prompt.lower():
                    return obj
        for obj, keywords in objects.items():
            for keyword in keywords[1:]:
                if keyword in prompt:
                    return obj
        return "object"