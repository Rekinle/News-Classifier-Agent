# news_classifier_gui.py
import tkinter as tk
from tkinter import scrolledtext
import requests


def classify_news(title, description):
    # 保持您原有的分类逻辑（完全本地调用）
    prompt = (
        "请将以下新闻分类为World、Sports、Business或Science/Tech。"
        "仅输出类别名称，不要任何其他文字，不要解释，不要标点符号。"
        f"标题：{title}"
        f"内容：{description}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:1.7b",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.0
        }
    )
    response.raise_for_status()
    return response.json()["response"].strip()


class NewsClassifierApp:
    def __init__(self, root):
        self.root = root
        root.title("新闻分类智能体")
        root.geometry("600x400")

        # 标题输入
        tk.Label(root, text="新闻标题:").pack(anchor="w", padx=10, pady=5)
        self.title_entry = tk.Entry(root, width=80)
        self.title_entry.pack(padx=10, fill="x")

        # 内容输入
        tk.Label(root, text="新闻内容:").pack(anchor="w", padx=10, pady=5)
        self.desc_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
        self.desc_text.pack(padx=10, fill="both", expand=True)

        # 分类按钮
        self.btn = tk.Button(root, text="开始分类", command=self.classify)
        self.btn.pack(pady=10)

        # 结果显示
        tk.Label(root, text="分类结果:").pack(anchor="w", padx=10, pady=5)
        self.result_var = tk.StringVar()
        self.result_label = tk.Label(root, textvariable=self.result_var, font=("Arial", 14, "bold"), fg="blue")
        self.result_label.pack(padx=10, pady=5)

    def classify(self):
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not title or not description:
            self.result_var.set("错误：标题或内容不能为空！")
            return

        try:
            self.result_var.set("正在分析...")
            root.update()
            result = classify_news(title, description)
            self.result_var.set(f"✅ 分类结果: {result}")
        except Exception as e:
            self.result_var.set(f"❌ 错误: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NewsClassifierApp(root)
    root.mainloop()