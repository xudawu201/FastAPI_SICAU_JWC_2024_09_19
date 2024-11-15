let WSocket = null;  // WebSocket对象，全局变量
let generation_info_dict = new Map(); // 存储排课信息的字典
let current_page = 1;  // 当前页码
let start_page = 1;  // 页码范围的起始页
const show_per_page = 50;  // 每页显示的排课信息条目数

// 开始排课函数
async function start_course_schedule() {
    WSocket = new WebSocket('/ws_course_schedule'); // 创建WebSocket连接
    const generation_progress_div = document.getElementById("generation_progress_div");
    generation_progress_div.innerHTML = ""; // 清空现有内容

    // 监听WebSocket消息
    WSocket.onmessage = function(event) {
        const response_data = JSON.parse(event.data); // 解析消息
        const generation_int = response_data.generation; // 当前进化代数
        const best_fitness_float = response_data.best_fitness; // 当前代数的最佳适应度

        // 将当前代数的排课信息存储到字典中
        generation_info_dict.set(generation_int, response_data.current_generation_info_dict);

        // 创建进度显示内容
        const progress_content_div = document.createElement("div");
        progress_content_div.innerHTML = `当前进化代数:${generation_int}，当前代最高适应度:${best_fitness_float}`;

        // 将新的进度信息添加到排课过程显示框
        generation_progress_div.appendChild(progress_content_div);
        // 点击显示具体排课信息
        progress_content_div.onclick = () => show_course_schedule_info(generation_int);

        // 自动滚动到最新的进度信息
        generation_progress_div.scrollTop = generation_progress_div.scrollHeight;
    }
}

// 停止排课函数
async function stop_course_schedule() {
    if (WSocket) {
        WSocket.close(); // 关闭WebSocket连接
        }
}


// 显示当前代排课信息总览
async function show_generation_course_schedule_summary_info(generation_int) {
    const generation_schedule_summary_info_div = document.getElementById("generation_schedule_summary_info_div");
    generation_schedule_summary_info_div.innerHTML = ""; // 清空现有内容

    // 获取当前代数的排课信息
    const CurrentScheduleInfo = generation_info_dict.get(generation_int);
            
    fitness_float = CurrentScheduleInfo["fitness_float"];
    total_assigned_course_number_int = CurrentScheduleInfo["total_assigned_course_number"];
    unassigned_room_list = CurrentScheduleInfo["unassigned_room_list"];
    unassigned_time_list = CurrentScheduleInfo["unassigned_time_list"];
    unassigned_teacher_list = CurrentScheduleInfo["unassigned_teacher_list"];
    unassigned_student_list = CurrentScheduleInfo["unassigned_student_list"];
    schedule_conflict_time_teacher = CurrentScheduleInfo["schedule_conflict_time_teacher"];
    schedule_conflict_time_student = CurrentScheduleInfo["schedule_conflict_time_student"];

    // 调整所有教室都被安排了的字符串
    if (unassigned_room_list =='All rooms assigned.'){
        unassigned_room_list = '';
    }

    // 创建进度显示内容
    const summary_content_div = document.createElement("div");
    summary_content_div.innerHTML = `<strong>当前代数:</strong>${generation_int}，<strong>适应度:</strong>${fitness_float} <br>`;
    summary_content_div.innerHTML += `<strong>总排课课程数:</strong>${total_assigned_course_number_int} <br>`;
    summary_content_div.innerHTML += `<strong>未安排课程教室:</strong>${unassigned_room_list} <br>`;
    summary_content_div.innerHTML += `<strong>未安排课程时间:</strong>${unassigned_time_list} <br>`;
    summary_content_div.innerHTML += `<strong>未安排上课教师:</strong>${unassigned_teacher_list} <br>`;
    summary_content_div.innerHTML += `<strong>未安排上课学生:</strong>${unassigned_student_list} <br>`;
    summary_content_div.innerHTML += `<strong>上课时间冲突教师:</strong>${schedule_conflict_time_teacher} <br>`;
    summary_content_div.innerHTML += `<strong>上课时间冲突学生:</strong>${schedule_conflict_time_student} <br>`;

    // 将新的进度信息添加到排课过程显示框
    generation_schedule_summary_info_div.appendChild(summary_content_div);
}


// 显示具体的排课信息
async function show_course_schedule_info(generation_int) {

    // 显示当前代排课总览
    show_generation_course_schedule_summary_info(generation_int)

    // 显示当前代详细排课信息    
    const schedule_info_div = document.getElementById("schedule_info_div");
    schedule_info_div.innerHTML = ""; // 清空现有内容
    
    // 显示当前代信息
    // 获取当前代数的排课信息
    const CurrentScheduleInfo = generation_info_dict.get(generation_int);
    if (CurrentScheduleInfo) {
        const total_assigned_time_numer_int = CurrentScheduleInfo["total_assigned_course_number"];
        const start_index = (current_page - 1) * show_per_page;
        const end_index = start_index + show_per_page;
        
        // 创建并显示当前代数和适应度信息
        const top_generation_info_div = document.createElement("div");
        top_generation_info_div.innerHTML = `当前代数: ${generation_int} 适应度: ${fitness_float}`;
        // 将当前代数和适应度信息添加到排课信息显示框的左上角
        schedule_info_div.appendChild(top_generation_info_div);

        const schedule_table = document.createElement("table");

        // 创建表头
        const header = schedule_table.insertRow();
        const headers = ["上课时间", "上课教室", "课程名称", "授课教师", "课程优先级", "选课学生", "上课时间冲突学生", "教师不可上课时间备注"];
        headers.forEach(header_text => {
            const th = document.createElement("th");
            th.innerHTML = header_text;
            header.appendChild(th);
        });

        // 获取排课数据并分页显示
        const schedule_list = Object.entries(CurrentScheduleInfo['room_assigned_course_schedule_dict']);
        const paginated_schedule = schedule_list.slice(start_index, end_index);

        // 创建表格行，填充排课信息
        paginated_schedule.forEach(([key, schedule_dict]) => {
            const row = schedule_table.insertRow();
            row.insertCell(0).innerHTML = schedule_dict.time;
            row.insertCell(1).innerHTML = schedule_dict.room;
            row.insertCell(2).innerHTML = schedule_dict.course;
            row.insertCell(3).innerHTML = schedule_dict.teacher;

            row.insertCell(4).innerHTML = schedule_dict.priority;
            row.insertCell(5).innerHTML = schedule_dict.enrolled_student;
            row.insertCell(6).innerHTML = schedule_dict.conflict;
            row.insertCell(7).innerHTML = schedule_dict.availability;
        });

        // 将排课表格添加到页面中
        schedule_info_div.appendChild(schedule_table);
        // 显示分页
        show_pagination(total_assigned_time_numer_int, generation_int);
    } 
    else {
        schedule_info_div.innerHTML = `未找到第 ${generation_int} 代的排课信息。`;
    }
}

// 显示分页功能
function show_pagination(total_items, generation_int) {
    const schedule_info_div = document.getElementById("schedule_info_div");
    const pagination_div = document.createElement("div");
    pagination_div.classList.add("pagination");

    const total_pages = Math.ceil(total_items / show_per_page);

    // 计算新的页码范围，使当前页位于中间
    const pages_in_view = 10; // 每次显示的最大页码数量
    let min_page = Math.max(1, current_page - Math.floor(pages_in_view / 2));
    let max_page = Math.min(total_pages, min_page + pages_in_view - 1);

    // 确保页码范围不会超出总页数
    if (max_page - min_page < pages_in_view - 1) {
        min_page = Math.max(1, max_page - pages_in_view + 1);
    }

    // 清空现有的分页按钮
    const existingPaginationDiv = schedule_info_div.querySelector(".pagination");
    if (existingPaginationDiv) {
        existingPaginationDiv.remove();
    }

    // 创建页码按钮
    for (let page = min_page; page <= max_page; page++) {
        const page_button = document.createElement("button");
        page_button.innerHTML = page;

        // 添加当前页的样式
        if (page === current_page) {
            page_button.disabled = true;  // 禁用当前页按钮
            // 设置css样式
            page_button.classList.add("current-page");
        }

        // 点击分页按钮，更新页码并显示对应内容
        page_button.onclick = function () {
            current_page = page;
            show_course_schedule_info(generation_int); // 重新显示信息
            // 滚动到底部
            schedule_info_div.scrollTop = schedule_info_div.scrollHeight;
        };

        pagination_div.appendChild(page_button);
    }

    // 添加分页到排课信息显示框
    schedule_info_div.appendChild(pagination_div);
}