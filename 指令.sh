# 下载 已完成
mkdir -p qa_project/data
wget -O qa_project/data/1.exam.json "https://NLP-course-cuhksz.github.io/Assignments/Assignment1/task1/data/1.exam.json"


#安装必须
pip install -r requirements.txt

#环境
export DEEPSEEK_API_KEY="sk-ed23ef1a37134535a8d93be537a575d0"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"

#跑
python run_eval.py --strategy baseline 
#baseline是跑了什么


python run_eval.py --strategy strict --model_name deepseek-chat
python run_eval.py --strategy cot --model_name deepseek-chat
python run_eval.py --strategy option_elimination --model_name deepseek-chat
python run_eval.py --strategy reflection --model_name deepseek-chat

# strict：看格式约束本身有没有收益
# cot：看推理链是否提升
# option_elimination：特别适合多选题
# reflection：看自检是否提升但是否更慢

python run_eval.py --strategy few_shot --model_name deepseek-chat
python run_eval.py --strategy multi_select_strict --model_name deepseek-chat

#参考下载
mkdir -p data/kb
wget -O data/kb/who_eml_2025.pdf "https://iris.who.int/server/api/core/bitstreams/17642505-ecd3-4940-a691-4f1dfa0d835a/content"

#rag
python run_eval.py --strategy rag --model_name deepseek-chat --kb_path data/kb
python run_eval.py --strategy rag_cot --model_name deepseek-chat --kb_path data/kb


python merge_metrics.py
python plot_results.py
