window.onload = async function() {
    const response = await fetch('/verify-token', {
        method: 'GET',
        credentials: 'include'  // 携带 HttpOnly Cookie
    });

    // 如果session有效，显示用户信息并保持在当前页面
    if (response.ok) {
        const result = await response.json();
        document.getElementById('message').innerText = result.message;
    } 
    // 如果session无效，跳回登录页面
    else {
        window.location.href = '/';
    }
}