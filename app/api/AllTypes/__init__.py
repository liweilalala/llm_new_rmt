import numpy as np
from prompts import conference_prompt, leader_speech_prompt, strategic_signing_prompt, exhibition_prompt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.LLM import create_task_loop

def calculate_levenshtein_distance(text1, text2):
    m, n = len(text1), len(text2)
    dp = np.zeros((m + 1, n + 1))

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    length = float(max(m, n))
    if length == 0.0:
        return 0
    else:
        return float(dp[m][n]) / length


class Conference:
    def generate(self, user_input: str):
        query_list = []
        for i in range(3):
            query = conference_prompt["prompts"][i].format(
                common_message=conference_prompt["common_message"],
                user_input=user_input)
            query_list.append(query)
        result_message = create_task_loop(query_list)
        if result_message is None:
            raise Exception("生成失败，请重试")
        return result_message["answer"]


class LeaderSpeech:
    def generate(self, user_input: str):
        prompt1 = leader_speech_prompt["prompts"][0].format(user_input=user_input)
        result_message = create_task_loop([prompt1] * 3)
        if result_message is None:
            raise Exception("生成失败，请重试")
        result_text = result_message["answer"]
        original_input_paragraphs = user_input.split("\n")
        result_paragraphs = original_input_paragraphs.copy()
        for i in range(len(original_input_paragraphs)):
            input_section = original_input_paragraphs[i]
            deleted = False
            if "谢谢" in input_section and len(input_section) < 150:
                result_paragraphs[i] = ""
                continue
            for delete_section in result1.split("\n"):
                similarity = calculate_levenshtein_distance(input_section, delete_section)
                if similarity < 0.8:
                    result_paragraphs[i] = ""
                    deleted = True
                    continue
            if deleted:
                continue
            key_words = ["我们"]
            for word in key_words:
                result_paragraphs[i] = result_paragraphs[i].replace(word, "")
        result_paragraphs = [section for section in result_paragraphs if section != ""]
        new_result = "\n\n".join(result_paragraphs)       # 正常的输出
        return new_result

if __name__ == "__main__":
    print(conference_prompt)