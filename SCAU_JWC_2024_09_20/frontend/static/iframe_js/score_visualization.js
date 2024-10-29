/*
 * @Author: xudawu
 * @Date: 2024-10-29 15:25:37
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-29 15:30:40
 */
async function show_iframe() {
    // 清除欢迎信息
    document.getElementById('welcome_message_div').style.display = 'none';

    // 创建 iframe
    var iframe = document.createElement('iframe');
    iframe.src = '/score_visualization';
    iframe.width = '98%';
    iframe.height = '100%';
    iframe.style.border = 'none';
    // 将 iframe 添加到内容区
    document.getElementById('content_div').appendChild(iframe);
}