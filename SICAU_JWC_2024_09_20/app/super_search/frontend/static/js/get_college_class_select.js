// 定义一个函数内变量,可以重新赋值
let college_class_dict = {};

// 页面加载完成后自动执行以下函数
window.onload = async function() {
    
    // 从 FastAPI 发送post请求学院和班级数据
    const response = await fetch('/filter_score', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
});
    // 获得数据
    college_class_dict = await response.json();

    // 填充学院下拉框
    const collegeSelect = document.getElementById('college');
    for (const college in college_class_dict) {
        const option = document.createElement('option');
        option.value = college;
        option.textContent = college;
        collegeSelect.appendChild(option);
    }

};

// 学院选择变化执行以下函数
async function update_class() {
    const collegeSelect = document.getElementById('college');
    const classSelect = document.getElementById('class');
    const courseTypeSelect = document.getElementById('corse_type');

    const selectedCollege = collegeSelect.value;
    // 初始化班级和课程类型下拉框
    classSelect.innerHTML = '<option value="">请选择班级</option>';
    courseTypeSelect.innerHTML = '<option value="">请选择课程性质</option>'; 
    
    // 如果选择了学院再填充班级下拉框
    if (selectedCollege) {
        college_class_dict[selectedCollege].forEach(cls => {
            const option = document.createElement('option');
            option.value = cls;
            option.textContent = cls;
            classSelect.appendChild(option);
        });
    }
}