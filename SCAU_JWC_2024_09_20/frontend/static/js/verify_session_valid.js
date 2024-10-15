/*
 * @Author: xudawu
 * @Date: 2024-10-14 17:05:28
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-15 15:31:41
 */
window.onload = async function() {
    const response = await fetch('/verify_cookie', {
        method: 'GET',
        credentials: 'include'  // 携带 HttpOnly Cookie
    });

    // 如果session有效，显示用户信息并保持在当前页面
    if (response.ok) {
        const result = await response.json();
        document.getElementById('message').innerText = result.message;
    } 
    // 如果session无效，弹出提示并跳回登录页面
    else {
        alert('登录状态已过期，点击确定跳转到登录页重新登录。');
        window.location.href = '/';
    }
}