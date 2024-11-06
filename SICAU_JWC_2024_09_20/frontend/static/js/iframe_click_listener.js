// 监听子页面的点击事件，并将点击事件的消息传到父页面
window.addEventListener('click', function() {
    window.parent.postMessage('hideMenu', '*');
});