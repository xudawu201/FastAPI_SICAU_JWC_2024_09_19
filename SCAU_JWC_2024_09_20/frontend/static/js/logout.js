/*
 * @Author: xudawu
 * @Date: 2024-10-12 16:33:34
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-14 15:30:29
 */
// 在页面hmtl加载完成后执行以下代码
document.addEventListener('DOMContentLoaded', function() {
    // 退出登录功能
    document.getElementById('logout_button').addEventListener('click', async function() {
        const response = await fetch('/logout', {
            method: 'POST',
            credentials: 'include',  // 发送请求时附带cookie
        });
        
        if (response.ok) {
            // 退出成功，重定向到登录页面
            window.location.href = '/';
        } else {
            console.error('Logout failed.');
        }
    });
});