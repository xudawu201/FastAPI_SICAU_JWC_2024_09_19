// 页面完全加载完成后时，通过后端验证 session_token 是否有效,访问 /verify-token路径，这是后端用于验证 session_token 的接口
window.onload = async function() {
    const response = await fetch('/verify-token', {
        method: 'GET',
        credentials: 'include'
    });
    // 如果session有效，跳转到登录成功页面
    if (response.ok) {
        window.location.href = '/login_success';
    } 
    // 如果session无效，保持在当前页面
    else {
        console.log('Invalid or expired token, staying on login page.');
    }
}