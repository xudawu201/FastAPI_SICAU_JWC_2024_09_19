// 获取按钮和滑出菜单元素
const userMenuButton = document.getElementById('user_info_button');
const userMenu = document.getElementById('userMenu');

// 点击个人账户按钮时显示或隐藏菜单
userMenuButton.addEventListener('click', function() {
    userMenu.classList.toggle('active'); // 切换显示状态
});

// 点击页面其他部分时隐藏菜单
window.addEventListener('click', function(event) {
    if (!userMenu.contains(event.target) && event.target !== userMenuButton) {
        userMenu.classList.remove('active');
    }
});

// 点击iframe页面时也隐藏菜单
window.addEventListener('message', function(event) {
    if (event.data === 'hideMenu') {
        userMenu.classList.remove('active');
    }
});