
<script src="{{ url_for('static', filename='js/socket.io.js') }}"></script>

// 初始化
let socket = io();

// DOM元素
let messageInput = document.getElementById('message-input');  
let modelSelect = document.getElementById('model-select');

// 加载模型列表
fetch('/models')
  .then(res => res.json())
  .then(models => {
    // 渲染模型选择框
  })

// 选择模型  
modelSelect.onchange = function() {
  socket.emit('update_model', {
    model: this.value
  });
}  

// 发送消息
document.getElementById('btn-msg-send').onclick = function() {

  let message = messageInput.value;
  console.log("click send message btn,msg: " + message)
  socket.emit('message', {
    message: message
  });

  // 添加消息到界面  
  addMessage('user', message);

}

// 接收响应 
socket.on('response', data => {
  addMessage('bot', data.message);
})

// 用量查询
setInterval(() => {
  socket.emit('get_usage');
}, 10000);

socket.on('usage', data => {
  // 更新用量信息界面
})


// 文件上传
document.getElementById('file-input').onchange = function() {
  let file = this.files[0];

  socket.emit('upload_file', file);
} 

socket.on('upload_progress', data => {
  // 更新上传进度  
})

socket.on('upload_result', data => {
  // 显示结果
})

// 共用的添加消息函数
function addMessage(type, message) {
  // ...
}