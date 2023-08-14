from flask import Flask, jsonify,render_template, request
from chatbot import ChatBot
from utils import load_config, validate_config
import logging.config
import json

# Load and validate configuration
config = load_config("config.yaml")
validate_config(config)

# Initialize chatbot
chatbot = ChatBot(config['openai']['api_key'], config['openai']['model'])

# Initialize Flask app and SocketIO
app = Flask(__name__)

# Configure logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('openai_chatbot')

@app.route('/')
def index():
    return render_template('index.html')

#选择模型
@app.route('/models')
def get_models():
  return jsonify(config['models'])

@app.route('/chat', methods=['POST'])
def chat():
  # 前端代码中已经将message json化了
  # body: JSON.stringify({message})
  # 后端要重新load出来
  data = json.loads(request.data)
  message = data['message']
  print(message)
  logger.debug('Message: %s', message)
  
  if not message:
    return {'error': 'Message cannot be empty'}
    
  response = chatbot.send_message(message)
  
  return {'message': response}

@app.route('/usage')
def usage():
    usage_info = chatbot.get_usage_info()
    # 需要把usage的json返回格式化好
    usage_info_format = json.dumps(usage_info,indent=2,ensure_ascii=False)
    print(usage_info_format)
    return {'usage_info': usage_info_format}

if __name__ == '__main__':
    app.run(debug=True)
