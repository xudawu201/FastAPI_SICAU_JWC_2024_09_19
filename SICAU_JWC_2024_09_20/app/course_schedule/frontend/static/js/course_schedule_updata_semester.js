/*
 * @Author: xudawu
 * @Date: 2024-12-18 16:33:26
 * @LastEditors: xudawu
 * @LastEditTime: 2024-12-18 17:23:06
 */// 页面加载完成后自动执行以下函数
async function load_semester() {
    
    // 从 FastAPI 发送post请求数据
    const response = await fetch('/load_semester', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    })

    // 获得数据
    semester_dict = await response.json();

    // 找到学期下拉框
    const semester_select = document.getElementById('select_semester_select');

    // 清空现有的选项
    while (semester_select.firstChild) {
        semester_select.removeChild(semester_select.firstChild);
    }

    // 获取semester_list
    const semester_list = semester_dict.semester_list;

    // 遍历semester_list中的每个学期
    semester_list.forEach(semester_str => {
        const option = document.createElement('option');
        option.value = semester_str;
        option.textContent = semester_str;
        semester_select.appendChild(option);
    });

};

// 确保页面加载完成后执行函数
window.onload = load_semester;

// 选择变化执行以下函数
async function update_semester() {
    // 找到学期下拉框
    const semester_select = document.getElementById('select_semester_select');

    // 获得元素的值
    semester_str = semester_select.value;
    
    const response = await fetch('/update_semester', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            semester_str: semester_str,
        })
    });
}