/*
 * @Author: xudawu
 * @Date: 2024-10-14 17:05:28
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-30 09:26:30
 */
// 页面完全加载完成后时，通过后端验证 session_token 是否有效,访问 /verify-token路径，这是后端用于验证 session_token 的接口
document.addEventListener('DOMContentLoaded', async function(){
    const response = await fetch('/verify_cookie', {
        method: 'GET',
        credentials: 'include'  // 携带 HttpOnly Cookie
    });

    if (response.redirected) {
        alert('登录状态已过期，点击确定跳转到登录页重新登录。');
        // 处理重定向
        window.location.href = response.url;  
    }
})