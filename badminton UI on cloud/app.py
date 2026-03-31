from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import cv2
import hashlib
import webbrowser

app = Flask(__name__)
CORS(app)  # 允许跨域访问（手机访问需要）

# 配置文件上传
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """主页：上传视频的界面"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """接收上传的视频文件"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if file and allowed_file(file.filename):
        # 用时间戳+哈希避免重名
        filename = hashlib.md5(file.filename.encode()).hexdigest() + '.mp4'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({
            'message': '上传成功',
            'filepath': filepath,
            'filename': filename
        }), 200
    
    return jsonify({'error': '文件格式不支持'}), 400

@app.route('/analyze/<filename>', methods=['GET'])
def analyze_video(filename):
    """分析视频：这里放你的TrackNet/YOLO逻辑"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # ========== 这里是你的分析代码入口 ==========
    # 例如：
    # results = tracknet_inference(filepath)
    # =======================================
    
    # 临时返回模拟数据（后续替换为真实分析结果）
    return jsonify({
        'status': '分析完成',
        'filename': filename,
        'shots': 42,           # 击球次数
        'smash_speed': 280,    # 最快杀球速度(km/h)
        'hotspot': '/static/result/hotmap.png'  # 热力图路径
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查：判断服务是否在运行"""
    return jsonify({'status': 'alive', 'message': '服务正常运行中'})

if __name__ == '__main__':
    # 关键：host='0.0.0.0' 让同一局域网的设备都能访问
    # debug=False 避免代码变动时自动重启（但开发时可设为True）
    webbrowser.open('http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
