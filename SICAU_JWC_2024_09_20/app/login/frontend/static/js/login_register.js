/*
 * @Author: xudawu
 * @Date: 2024-10-12 11:52:07
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-18 14:41:08
 */
// 登录表单提交时阻止默认提交行为并使用 fetch 处理请求
async function handleLoginSubmit(event) {
    event.preventDefault();  // 阻止默认表单提交
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorMessage = document.getElementById('login-error-message');

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password})
    });

    const result = await response.json();
    
    if (result.login_flag==='true') {
        window.location.href = '/main';  // 登录成功后跳转
    } 
    else if(result.have_user==='false'){
        errorMessage.textContent = '用户名不存在';
        errorMessage.style.display = 'block';  // 显示错误信息
    }
    else if(result.have_user==='true' && result.login_flag==='false'){
        errorMessage.textContent = '密码错误';
        errorMessage.style.display = 'block';  // 显示错误信息
    }
}

// 注册表单提交时阻止默认提交行为并使用 fetch 处理请求
async function handleRegisterSubmit(event) {
    event.preventDefault();  // 阻止默认表单提交
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const errorMessage = document.getElementById('register-error-message');

    if (password !== confirmPassword) {
        errorMessage.textContent = '两次密码不匹配';
        errorMessage.style.display = 'block';
        return;
    }

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password})
    });

    const result = await response.json();

    if (result.already_name_flag ==='true'){
        errorMessage.textContent = '注册失败，该用户名已被注册';
        errorMessage.style.display = 'block';
    }
    else if (result.already_name_flag ==='false'){
        errorMessage.style.display = 'block';
        alert(`${result.username} 注册成功，请登录`);
        toggleForms();
    }
}

// 切换登录和注册表单
function toggleForms() {
    const loginForm = document.getElementById('login_div');
    const registerForm = document.getElementById('register_div');
    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    } 
    else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    }
}

// 监听表单提交事件
document.getElementById('login_form').addEventListener('submit', handleLoginSubmit);
document.getElementById('register_form').addEventListener('submit', handleRegisterSubmit);