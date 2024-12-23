/*
 * @Author: xudawu
 * @Date: 2024-10-29 15:25:37
 * @LastEditors: xudawu
 * @LastEditTime: 2024-11-14 10:45:55
 */
async function show_course_schedule_iframe() {

    // 禁用菜单栏的链接
    const button = document.getElementById("left_menu_ul_id");
    // 禁用点击
    button.style.pointerEvents = "none"; 
    // 可选：更改链接透明度以表示禁用状态
    button.style.opacity = "0.5"; 

    // 显示加载提示
    const loadingDiv = document.getElementById('loading_div');
    loadingDiv.style.display = 'block';

    // 创建 iframe
    var iframe = document.createElement('iframe');
    
    iframe.src = '/course_schedule';
    iframe.width = '98%';
    iframe.height = '100%';
    iframe.style.border = 'none';
    
    // 清空内容区，防止重复添加 iframe
    document.getElementById('content_div').innerHTML = '';

    // 将加载提示和 iframe 添加到内容区
    document.getElementById('content_div').appendChild(loadingDiv);
    document.getElementById('content_div').appendChild(iframe);

    // 等待 iframe 加载完成后隐藏加载提示
    iframe.onload = function() {
        loadingDiv.style.display = 'none';

        // 重新启用链接
        // 启用点击
        button.style.pointerEvents = "auto"; 
        // 恢复透明度
        button.style.opacity = "1";
    };

}
