/*
 * @Author: xudawu
 * @Date: 2024-10-14 17:05:28
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-30 08:57:27
 */
// 页面完全加载完成后时，通过后端验证 session_token 是否有效,访问 /verify-token路径，这是后端用于验证 session_token 的接口
document.addEventListener('DOMContentLoaded', async function(){
    const response = await fetch('/verify_cookie_login', {
        method: 'GET',
        credentials: 'include'
    });
    // 处理重定向
    if (response.redirected) {
        window.location.href = response.url;
    }
})