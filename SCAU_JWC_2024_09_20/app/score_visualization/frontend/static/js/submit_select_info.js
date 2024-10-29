/*
 * @Author: xudawu
 * @Date: 2024-10-28 10:20:55
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-29 13:20:54
 */
// 班级选择变化执行以下函数
async function submit_select_info() {
    // 获得元素
    const college_select_element = document.getElementById('college');
    const class_select_element = document.getElementById('class');
    const course_type_select_element = document.getElementById('corse_type');
    
    // 再后端返回数据前锁定筛选框
    college_select_element.disabled = true;
    class_select_element.disabled = true;
    course_type_select_element.disabled = true;

    // 获得元素的值
    const college_select_str = college_select_element.value;
    const class_select_str = class_select_element.value;
    const course_type_select_str = course_type_select_element.value;
    
    // 如果都有值
    if (college_select_str!='' && class_select_str!='' && course_type_select_str!='') {
        // 将选择的学院和班级值提交到 FastAPI 后端
        const response = await fetch('/submit_select_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                college_name_str: college_select_str,
                class_name_str: class_select_str,
                course_type_name_str: course_type_select_str
            })
        });
        
        // 获取返回的 JSON 数据
        const data = await response.json();

        // 更新图表的 HTML
        const line_chart_div = document.getElementById('line_chart_div');
        line_chart_div.innerHTML = data.line_chart_html; // 更新第一个图表的 HTML

        const group_line_chart_div = document.getElementById('group_line_chart_div');
        group_line_chart_div.innerHTML = data.group_line_chart_html; // 更新第二个图表的 HTML

        // 执行图表更新新插入的脚本
        executeScripts(line_chart_div);
        executeScripts(group_line_chart_div);

    }

    // 无论成功之前if条件满足与否都解锁筛选框
    college_select_element.disabled = false;
    class_select_element.disabled = false;
    course_type_select_element.disabled = false;

};

// 执行新插入的脚本
function executeScripts(container) {
    const scripts = container.getElementsByTagName('script');
    for (let script of scripts) {
        const newScript = document.createElement('script');
        // 将脚本内容放入新元素中
        newScript.textContent = script.innerHTML; 
        // 将新元素添加到 DOM 中
        document.body.appendChild(newScript); 
    }
}