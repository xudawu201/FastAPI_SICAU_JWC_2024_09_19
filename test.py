<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>欢迎页面</title>
</head>
<body>
    <h1 id="greeting">Hey，欢迎来到我们的网站！</h1>
    <button onclick="changeGreeting()">换一个问候语</button>

    <script>
        function changeGreeting() {
            const greetingElement = document.getElementById('greeting');
            if (greetingElement.textContent === 'Hey，欢迎来到我们的网站！') {
                greetingElement.textContent = 'Hello, welcome to our website!';
            } else {
                greetingElement.textContent = 'Hey，欢迎来到我们的网站！';
            }
        }
    </script>
</body>
</html>
