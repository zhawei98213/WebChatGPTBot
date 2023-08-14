/* static/js/main.js */

//将消息容器的获取移入 DOMContentLoaded 回调内,确保在 DOM 加载后获取
document.addEventListener('DOMContentLoaded', async () => {
    const chatForm = document.getElementById('chat-form');

    // 绑定发送消息的表单提交事件
    chatForm.addEventListener('submit', sendMessage);

    // 初始化
    await init();
});

// 初始化调用
async function init() {

    // 5分钟的毫秒数
    const interval = 5 * 60 * 1000;

    // 获取用量
    await getUsage();

    // 每隔一段时间调用
    setInterval(() => {
        // 计算当前时间
        const now = new Date();
        // 应用8小时时区偏移
        now.setTime(now.getTime() + 8 * 60 * 60 * 1000);

        console.log("Call getUsage func every 5 mins");
        getUsage();

    }, interval);

}

// 发送消息的异步函数
async function sendMessage(event) {
    event.preventDefault();
    const messageInput = document.getElementById('message-input');
    const chatMsg = document.getElementById('chat-messages');

    chatMsg.autoScroll = true;

    // 消息容器滚动事件处理
    chatMsg.addEventListener('scroll', function () {
        // 用户手动滚动时取消自动滚动
        chatMsg.autoScroll = false;
    });

    const message = messageInput.value;
    messageInput.value = '';

    const userMessage = document.createElement('div');
    //用户在左边显示
    userMessage.classList.add('user-message');
    userMessage.textContent = `User: ${message}`;
    chatMsg.appendChild(userMessage);

    // 调用后端API发送消息
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    });

    // 获取并处理响应
    const data = await response.json();
    // 在聊天界面添加一条新消息 
    const botMessage = document.createElement('div');
    //机器人在右边显示
    botMessage.classList.add('bot-message');
    botMessage.textContent = `ChatGPT: ${data.message}`;
    chatMsg.appendChild(botMessage);

    // 检查是否需要自动滚动
    if (chatMsg.autoScroll) {
        chatMsg.scrollTop = chatMsg.scrollHeight;;
    }

    // 清空输入
    messageInput.value = '';

}

// 获取用量信息
async function getUsage() {

    const usageInfo = document.getElementById('usage-info');

    const response = await fetch('/usage');
    const data = await response.json();

    // 先转换成json格式
    const json = JSON.parse(data.usage_info);
    // 调用函数构建表格内容
    const table = buildUsageTable(json);

    // 插入页面  
    usageInfo.innerHTML = table;

}

// 添加构建表格的函数
function buildUsageTable(data) {
    // 获取 data 数组
    const records = data.data;
    // 构建表格时添加类名 
    let table = '<table class="usage-table">';

    table += '<tr class="header">';
    table += '<th class="col-time">Time</th>';
    // ...

    table += '<th>Requests</th><th>Tokens</th></tr>';

    records.forEach(r => {
        // 创建 Date 对象
        const date = new Date(r.aggregation_timestamp * 1000);
        // 北京时间时区偏移
        // 应用时区偏移  
        date.setMinutes(date.getMinutes() + 480);
        // 格式化日期时间
        const formatted = date.toISOString().slice(0, 19).replace('T', ' ');

        table += `
            <tr>
            <td>${formatted}</td>
            <td>${r.n_requests}</td>  
            <td>${r.n_generated_tokens_total}</td>
            </tr>
      `;
    });

    table += '</table>';

    return table;
}