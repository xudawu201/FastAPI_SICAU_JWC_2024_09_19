/*
 * @Author: xudawu
 * @Date: 2024-10-14 17:05:28
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-29 18:55:36
 */
// 页面完全加载完成后时，通过后端验证 session_token 是否有效,访问 /verify-token路径，这是后端用于验证 session_token 的接口
document.addEventListener('DOMContentLoaded', async function(){
    const response = await fetch('/verify_cookie', {
        method: 'GET',
        credentials: 'include'
    });
    // 如果session有效，跳转到登录成功页面
    if (response.ok) {
        window.location.href = '/main';
    } 
    // 如果session无效，保持在当前页面
    else {
        console.log('Invalid or expired token, staying on login page.');
    }
})