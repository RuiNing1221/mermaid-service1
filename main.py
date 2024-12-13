from flask import Flask, request, jsonify
import time
import subprocess
import os

app = Flask(__name__)

@app.route('/api/upload', methods=['POST'])
def upload_markdown():
    content = request.get_data(as_text=True)
    time_name = str(int(time.time()))
    file_name = time_name + ".md"
    
    # 创建临时目录
    os.makedirs('/tmp/data', exist_ok=True)
    
    file_path = f"/tmp/data/{file_name}"
    svg_path = f"/tmp/data/{file_name}-1.svg"
    
    # 防止格式不对
    if '```mermaid' not in content:
        content = '```mermaid\n' + content + '\n```'
    
    # 写入 Markdown 文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 生成 SVG
    try:
        subprocess.run([
            'mmdc', 
            '-i', file_path,
            '-o', svg_path
        ], check=True)
        
        # 读取 SVG 内容
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        return jsonify({
            "message": "Markdown 文件已保存",
            "svg_content": svg_content
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": str(e)
        }), 400

# Vercel 要求
def main(request):
    return app(request)
