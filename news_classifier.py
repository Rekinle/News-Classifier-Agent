import pandas as pd
import requests
import random
import numpy as np


def classify_news(title: str, description: str) -> str:
    """
    使用Qwen3:1.7b模型进行新闻分类，严格限制输出为四个类别之一
    """
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

    output = response.json()["response"].strip()
    valid_categories = ["World", "Sports", "Business", "Science/Tech"]
    for category in valid_categories:
        if output.startswith(category):
            return category
    return "Unknown"


def main():
    # 读取CSV文件
    df = pd.read_csv("test.csv")

    # 映射class_index到类别名称
    class_map = {
        1: "World",
        2: "Sports",
        3: "Business",
        4: "Science/Tech"
    }

    # 添加真实类别列
    df["real_category"] = df["Class Index"].map(class_map)

    # 随机选择5条新闻
    sample_size = min(5, len(df))
    sample_df = df.sample(n=sample_size, random_state=42)

    # 存储结果
    results = []

    print("=" * 60)
    print("新闻分类结果 (随机5条) - 准确率: {:.0%}".format(0))
    print("=" * 60)

    # 对每条新闻进行分类
    for _, row in sample_df.iterrows():
        predicted = classify_news(row["Title"], row["Description"])
        correct = predicted == row["real_category"]

        results.append({
            "title": row["Title"],
            "real": row["real_category"],
            "predicted": predicted,
            "correct": correct
        })

        # 打印每条新闻结果
        print(f"标题: {row['Title'][:50]}{'...' if len(row['Title']) > 50 else ''}")
        print(f"真实类别: {row['real_category']}")
        print(f"预测类别: {predicted}")
        print(f"准确: {'✓' if correct else '✗'}")
        print("-" * 50)

    # 计算准确率
    correct_count = sum(1 for r in results if r["correct"])
    accuracy = correct_count / len(results)

    # 重新打印标题行显示准确率
    print("\n" + "=" * 60)
    print(f"分类准确率: {accuracy:.0%} ({correct_count}/{len(results)})")
    print("=" * 60)


if __name__ == "__main__":
    main()