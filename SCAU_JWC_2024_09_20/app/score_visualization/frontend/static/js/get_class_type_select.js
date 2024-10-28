/*
 * @Author: xudawu
 * @Date: 2024-10-28 10:06:08
 * @LastEditors: xudawu
 * @LastEditTime: 2024-10-28 10:06:41
 */
// 班级选择变化执行以下函数
async function update_class_type() {
    const collegeSelect = document.getElementById('college');
    const class_selected = document.getElementById('class');
    const selectedCollege = collegeSelect.value;
    const selectedClass = class_selected.value;
    
    // 先初始化课程类型选项
    const corse_type_select = document.getElementById('corse_type');
    corse_type_select.innerHTML = '<option value="">请选择课程性质</option>';

    if (selectedCollege && selectedClass) {
        // 将选择的学院和班级值提交到 FastAPI 后端
        const response = await fetch('/submit_class_name', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                college_str: selectedCollege,
                class_str: selectedClass
            })
        });

        // 获得后端数据
        const result = await response.json();
        
        // 如果选择了班级再填充课程类型下拉框
        if (selectedClass) {
            result.course_type_list.forEach(cls => {
                const option = document.createElement('option');
                option.value = cls;
                option.textContent = cls;
                corse_type_select.appendChild(option);
            });
        }
    }

};