// 退出登录功能
document.getElementById('logout-btn').addEventListener('click', async function() {
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