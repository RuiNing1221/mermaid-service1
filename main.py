from flask import Flask, request, send_from_directory
import time
import subprocess
import os

app = Flask(__name__)

# 确保数据目录存在
os.makedirs('/app/data', exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_markdown():
    content = request.get_data(as_text=True)
    time_name = str(int(time.time()))
    file_name = time_name + ".md"
    
    # 防止格式不对
    if '```mermaid' not in content:
        content = '```mermaid\n' + content + '\n```'
    
    file_path = f"/app/data/{file_name}"
    svg_path = f"/app/data/{file_name}-1.svg"
    
    # 写入 Markdown 文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 生成 SVG
    result = subprocess.run([
        'mmdc', 
        '-p', 'puppeteer-config.json', 
        '-c', 'config.json', 
        '-i', file_path,
        '-o', svg_path
    ], capture_output=True, text=True)
    
    # 检查命令是否成功
    if result.returncode != 0:
        return f"Error: {result.stderr}", 400
    
    # 返回 SVG 文件名
    return {
        "message": "Markdown 文件已保存",
        "svg_filename": f"{file_name}-1.svg"
    }

@app.route('/svg/<filename>', methods=['GET'])
def get_svg(filename):
    return send_from_directory("/app/data", filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
