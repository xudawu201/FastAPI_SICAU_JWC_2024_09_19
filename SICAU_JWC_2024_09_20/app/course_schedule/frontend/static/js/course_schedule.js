let WSocket = null;  // WebSocket对象，全局变量
let generation_info_dict = new Map(); // 存储排课信息的字典
let current_page = 1;  // 当前页码
let start_page = 1;  // 页码范围的起始页
const show_per_page = 25;  // 每页显示的排课信息条目数
// 选择的当前代
let cur_generation_int = -1;
// 当前适应度
let cur_fitness_float = -1;

// 可视化分页当前页码
let visualize_current_page = 1; 
// 可视化分页每页显示的条目数
const visualize_show_per_page = 10;
// 每次显示的最大页码数量
const pages_in_view = 10;

// 快速开始排课函数
async function quick_start_course_schedule() {

    // 找到学期下拉框
    const semester_select = document.getElementById('select_semester_select');

    // 检查是否有当前选中
    if (!semester_select.value) {
        alert('请先选择一个学期');
        return;
    }

    WSocket = new WebSocket('/ws_course_schedule_quick'); // 创建WebSocket连接

    const generation_progress_div = document.getElementById("generation_progress_div");
    generation_progress_div.innerHTML = ""; // 清空现有内容
    // 显示变异进化信息
    const mutate_progress_div = document.getElementById("mutate_progress_div");
    mutate_progress_div.innerHTML = ""; // 清空现有内容

    // 定义消息队列和最大队列大小
    const mutateMessageQueue = [];
    const generationMessageQueue = [];
    const maxQueueSize = 100; // 队列最大容量

    // 添加消息到队列并更新显示
    function addToQueue(queue, message, displayDiv, renderCallback) {
        queue.push(message);
        if (queue.length > maxQueueSize) {
            queue.shift(); // 删除最早的消息
        }

        // 清空并重新渲染显示内容
        displayDiv.innerHTML = "";
        queue.forEach((msg) => {
            const messageDiv = document.createElement("div");
            renderCallback(messageDiv, msg);
            displayDiv.appendChild(messageDiv);
        });

        // 自动滚动到最新的内容
        displayDiv.scrollTop = displayDiv.scrollHeight;
    }

    // 监听WebSocket消息
    WSocket.onmessage = function(event) {
        const response_data = JSON.parse(event.data); // 解析消息
        if('process_message' in response_data) {
            // 获取消息
            const process_message = response_data.process_message;
            addToQueue(mutateMessageQueue, process_message, mutate_progress_div, (div, msg) => {
                div.innerHTML = `${msg}`; // 更新变异进化信息
            });
        } 
        else if('generation' in response_data) {
            const generation_int = response_data.generation; // 当前进化代数
            const best_fitness_float = response_data.best_fitness; // 当前代数的最佳适应度

            // 将当前代数的排课信息存储到字典中
            generation_info_dict.set(generation_int, response_data.current_generation_info_dict);
            
            // 创建进度显示内容
            const generation_message = {
                generation: generation_int,
                best_fitness: best_fitness_float,
            };
            addToQueue(generationMessageQueue, generation_message, generation_progress_div, (div, msg) => {
                div.innerHTML = `当前进化代数:${msg.generation}，当前代最高适应度:${msg.best_fitness}`;
                div.onclick = () => show_course_schedule_info(msg.generation); // 绑定点击事件
            });
            // 实时显示排课信息
            visualize_schedule(generation_int);
        }
    }
}

// 更优开始排课函数
async function better_start_course_schedule() {

    // 找到学期下拉框
    const semester_select = document.getElementById('select_semester_select');

    // 检查是否有当前选中
    if (!semester_select.value) {
        alert('请先选择一个学期');
        return;
    }

    WSocket = new WebSocket('/ws_course_schedule_better'); // 创建 WebSocket 连接

    const generation_progress_div = document.getElementById("generation_progress_div");
    generation_progress_div.innerHTML = ""; // 清空现有内容
    const mutate_progress_div = document.getElementById("mutate_progress_div");
    mutate_progress_div.innerHTML = ""; // 清空现有内容

    // 定义消息队列和最大队列大小
    const mutateMessageQueue = [];
    const generationMessageQueue = [];
    const maxQueueSize = 100; // 队列最大容量

    // 添加消息到队列并更新显示
    function addToQueue(queue, message, displayDiv, renderCallback) {
        queue.push(message);
        if (queue.length > maxQueueSize) {
            queue.shift(); // 删除最早的消息
        }

        // 清空并重新渲染显示内容
        displayDiv.innerHTML = "";
        queue.forEach((msg) => {
            const messageDiv = document.createElement("div");
            renderCallback(messageDiv, msg);
            displayDiv.appendChild(messageDiv);
        });

        // 自动滚动到最新的内容
        displayDiv.scrollTop = displayDiv.scrollHeight;
    }

    // 监听 WebSocket 消息
    WSocket.onmessage = function (event) {
        const response_data = JSON.parse(event.data); // 解析消息

        if ('process_message' in response_data) {
            // 获取消息
            const process_message = response_data.process_message;
            addToQueue(mutateMessageQueue, process_message, mutate_progress_div, (div, msg) => {
                div.innerHTML = `${msg}`; // 更新变异进化信息
            });
        } 
        else if ('generation' in response_data) {
            const generation_int = response_data.generation; // 当前进化代数
            const best_fitness_float = response_data.best_fitness; // 当前代数的最佳适应度

            // 将当前代数的排课信息存储到字典中
            generation_info_dict.set(generation_int, response_data.current_generation_info_dict);
            
            // 创建进度显示内容
            const generation_message = {
                generation: generation_int,
                best_fitness: best_fitness_float,
            };
            addToQueue(generationMessageQueue, generation_message, generation_progress_div, (div, msg) => {
                div.innerHTML = `当前进化代数:${msg.generation}，当前代最高适应度:${msg.best_fitness}`;
                div.onclick = () => show_course_schedule_info(msg.generation); // 绑定点击事件
            });
            // 实时显示排课信息
            visualize_schedule(generation_int);
        }
    }
}

// 停止排课函数
async function stop_course_schedule() {
    if (WSocket) {
        WSocket.close(); // 关闭 WebSocket 连接
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
    unassigned_course_dict = CurrentScheduleInfo["unassigned_course_dict"];
    unassigned_student_list = CurrentScheduleInfo["unassigned_student_list"];
    schedule_conflict_time_teacher = CurrentScheduleInfo["schedule_conflict_time_teacher"];
    schedule_conflict_time_student = CurrentScheduleInfo["schedule_conflict_time_student"];

    // 不正常的排课信息
    unnormal_schedule_str = CurrentScheduleInfo["unnormal_schedule_str"];
    unnormal_schedule_teacher_day_str = CurrentScheduleInfo["unnormal_schedule_teacher_day_str"];
    unnormal_schedule_teacher_week_str = CurrentScheduleInfo["unnormal_schedule_teacher_week_str"];

    // 创建进度显示内容
    const summary_content_div = document.createElement("div");
    // 为进度显示内容添加样式类名
    summary_content_div.className = "schedule_summary_div";

    summary_content_div.innerHTML = `<strong>当前代数:</strong>${generation_int}，<strong>适应度:</strong>${fitness_float} <br/>`;
    summary_content_div.innerHTML += `<strong>总排课课程数:</strong>${total_assigned_course_number_int} <br/>`;

    
    summary_content_div.innerHTML += `<strong>上课时间冲突学生:</strong><br/>`;
    summary_content_div.innerHTML += `${schedule_conflict_time_student} <br/>`;
    
    summary_content_div.innerHTML += `<strong>被安排在教师不可上课时间的教师:</strong><br/>`;
    summary_content_div.innerHTML += `${schedule_conflict_time_teacher} <br/>`;

    summary_content_div.innerHTML += `<strong>课程安排次数不合理的:</strong><br/>`;
    summary_content_div.innerHTML += `${unnormal_schedule_str} <br/>`;
    summary_content_div.innerHTML += `<strong>教师一天上课次数大于等于3讲:</strong><br/>`;
    summary_content_div.innerHTML += `${unnormal_schedule_teacher_day_str} <br/>`;
    summary_content_div.innerHTML += `<strong>教师一周上课次数大于12讲:</strong><br/>`;
    summary_content_div.innerHTML += `${unnormal_schedule_teacher_week_str} <br/>`;
    
    summary_content_div.innerHTML += `<strong>未安排课程教室:</strong><br/>`;
    summary_content_div.innerHTML += `${unassigned_room_list} <br/>`;
    
    summary_content_div.innerHTML += `<strong>未安排排课课程:</strong><br/>`;
    // 遍历字典添加数据
    Object.entries(unassigned_course_dict).forEach(([key, value]) => {
        summary_content_div.innerHTML += `${value} <br/>`;
    });
    summary_content_div.innerHTML += `<strong>未安排上课学生:</strong><br/>`;
    summary_content_div.innerHTML += `${unassigned_student_list} <br/>`;
    
    summary_content_div.innerHTML += `<strong>未安排课程时间:</strong><br/>`;
    summary_content_div.innerHTML += `${unassigned_time_list} <br/>`;
    
    // 将新的进度信息添加到排课过程显示框
    generation_schedule_summary_info_div.appendChild(summary_content_div);
}


// 显示具体的排课信息
async function show_course_schedule_info(generation_int) {

    // 显示当前代排课总览
    show_generation_course_schedule_summary_info(generation_int)

    // 调用可视化函数
    visualize_schedule(generation_int);

    // 设置全局变量中当前代数更新
    cur_generation_int = generation_int;

    // 显示当前代详细排课信息    
    const schedule_info_div = document.getElementById("schedule_info_div");
    schedule_info_div.innerHTML = ""; // 清空现有内容
    
    // 显示当前代信息
    // 获取当前代数的排课信息
    const CurrentScheduleInfo = generation_info_dict.get(generation_int);
    if (CurrentScheduleInfo) {
        
        // 创建并显示当前代数和适应度信息
        const fitness_float = CurrentScheduleInfo["fitness_float"];
        // 更新适应度用于后续下载文件命名使用
        cur_fitness_float = fitness_float;
        const top_generation_info_div = document.createElement("div");
        top_generation_info_div.innerHTML = `当前代数: ${generation_int} 适应度: ${fitness_float}`;
        // 将当前代数和适应度信息添加到排课信息显示框的左上角
        schedule_info_div.appendChild(top_generation_info_div);

        const schedule_table = document.createElement("table");

        // 创建表头
        const header = schedule_table.insertRow();
        const headers = ["上课周数","上课星期","上课时间","校区","上课教室","排课类别","课程名称", "授课教师id","课程id","教室id","课程总学时要求","已排总学时","本周排课次数","已排学时和要求学时的距离","教师当天上课讲数","教师本周上课讲数","课程优先级", "选课学生", "教师不可上课时间段","上课时间冲突学生", "是否处于教师不可上课时间"];
        headers.forEach(header_text => {
            const th = document.createElement("th");
            th.innerHTML = header_text;
            header.appendChild(th);
        });

        const total_assigned_time_numer_int = CurrentScheduleInfo["total_assigned_course_number"];
        const start_index = (current_page - 1) * show_per_page;
        const end_index = Math.min(start_index + show_per_page, total_assigned_time_numer_int);

        // 获取排课数据并分页显示
        const schedule_list = Object.entries(CurrentScheduleInfo['room_assigned_course_schedule_dict']);
        const paginated_schedule = schedule_list.slice(start_index, end_index);

        // 创建表格行，填充排课信息
        paginated_schedule.forEach(([key, schedule_dict]) => {
            const row = schedule_table.insertRow();
            row.insertCell(0).innerHTML = schedule_dict.week;
            row.insertCell(1).innerHTML = schedule_dict.day;
            row.insertCell(2).innerHTML = schedule_dict.time;
            row.insertCell(3).innerHTML = schedule_dict.campus_area_str;

            row.insertCell(4).innerHTML = schedule_dict.room;
            row.insertCell(5).innerHTML = schedule_dict.schedule_course_type;
            row.insertCell(6).innerHTML = schedule_dict.course;
            row.insertCell(7).innerHTML = schedule_dict.teacher;

            row.insertCell(8).innerHTML = schedule_dict.course_id;
            row.insertCell(9).innerHTML = schedule_dict.room_id;

            row.insertCell(10).innerHTML = schedule_dict.cur_schedule_total_study_hour_float;
            row.insertCell(11).innerHTML = schedule_dict.cur_study_hour;
            row.insertCell(12).innerHTML = schedule_dict.schedule_week_count_int;
            row.insertCell(13).innerHTML = schedule_dict.study_hour_distance_float;

            row.insertCell(14).innerHTML = schedule_dict.course_teacher_day_study_hour_str;
            row.insertCell(15).innerHTML = schedule_dict.course_teacher_week_study_hour_str;

            row.insertCell(16).innerHTML = schedule_dict.priority;
            row.insertCell(17).innerHTML = schedule_dict.enrolled_student;
            row.insertCell(18).innerHTML = schedule_dict.unavailable_timeslots_teacher;
            row.insertCell(19).innerHTML = schedule_dict.conflict;

            row.insertCell(20).innerHTML = schedule_dict.availability;
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


// 可视化排课信息
async function visualize_schedule(generation_int) {
    const schedule_visualization_div = document.getElementById("schedule_visualization_div");
    schedule_visualization_div.innerHTML = ""; // 清空现有内容
    
    // 获取当前代数的排课信息
    const CurrentScheduleInfo = generation_info_dict.get(generation_int);
    if (!CurrentScheduleInfo) {
        schedule_visualization_div.innerHTML = `<div class="schedule-header">未找到第 ${generation_int} 代的排课信息。</div>`;
        return;
    }
    
    // 创建并显示当前代数和适应度信息
    const fitness_float = CurrentScheduleInfo["fitness_float"];
    const visualize_top_generation_info_div = document.createElement("div");
    visualize_top_generation_info_div.className = "visualize_top_generation_info_div";

    visualize_top_generation_info_div.innerHTML = `当前代数: ${generation_int} 适应度: ${fitness_float} <br>`;
    schedule_visualization_div.appendChild(visualize_top_generation_info_div);

    const assigned_schedule = Object.values(CurrentScheduleInfo['room_assigned_course_schedule_dict']);
    const unique_rooms = [...new Set(assigned_schedule.map(s => s.room))];
    const unique_times = [...new Set(assigned_schedule.map(s => `${s.week}, ${s.day}, ${s.time}`))];

    unique_rooms.sort();
    unique_times.sort();

    // 创建动态网格容器
    const gridContainer = document.createElement("div");
    gridContainer.className = "schedule-grid";
    gridContainer.style.gridTemplateColumns = `repeat(${unique_rooms.length + 1}, auto)`;

    // 填充横纵坐标和数据
    gridContainer.appendChild(createHeaderCell("time/room", "schedule-header"));
    unique_rooms.forEach(room => gridContainer.appendChild(createHeaderCell(room, "schedule-header-horizontal")));
    
    // 分页逻辑：计算当前页面的起始索引和结束索引
    const startIndex = (visualize_current_page - 1) * visualize_show_per_page;
    const endIndex = Math.min(startIndex + visualize_show_per_page, unique_times.length);

    // 只显示当前页面的数据
    const currentTimesToDisplay = unique_times.slice(startIndex, endIndex);

    currentTimesToDisplay.forEach(time => {
        gridContainer.appendChild(createHeaderCell(time, "schedule-header-vertical"));
        unique_rooms.forEach(room => {
            const cellData = assigned_schedule.find(s => `${s.week}, ${s.day}, ${s.time}` === time && s.room === room);
            if (cellData) {
                let conflicts_info_dict = {
                    teacher_is_unavailable: false,
                    student_is_conflict: false,
                };
                if (cellData.availability != '') {
                    conflicts_info_dict.teacher_is_unavailable = true;
                }
                if (cellData.conflict != '') {
                    conflicts_info_dict.student_is_conflict = true;
                }
                conflicts_info_dict.schedule_course_type = cellData.schedule_course_type;
                conflicts_info_dict.schedule_week_count = cellData.schedule_week_count_int;
                conflicts_info_dict.is_schedule = cellData.course;
                conflicts_info_dict.study_hour_distance_float = cellData.study_hour_distance_float;
                conflicts_info_dict.is_continuous_schedule = cellData.is_contitueous_course_bool;
                
                gridContainer.appendChild(createScheduleCell(cellData.course, cellData.teacher, conflicts_info_dict));
            } else {
                gridContainer.appendChild(createEmptyCell());
            }
        });
    });
    // 将网格容器添加到页面中
    schedule_visualization_div.appendChild(gridContainer);

    // 调用分页函数
    visualization_pagination(unique_times.length, generation_int);
}

// 可视化显示的分页
function visualization_pagination(total_items, generation_int) {
    const schedule_info_div = document.getElementById("schedule_visualization_div");
    const pagination_div = document.createElement("div");
    pagination_div.classList.add("visualization_pagination");

    const total_pages = Math.ceil(total_items / visualize_show_per_page);

    // 计算新的页码范围，使当前页位于中间
    let min_page = Math.max(1, visualize_current_page - Math.floor(pages_in_view / 2));
    let max_page = Math.min(total_pages, min_page + pages_in_view - 1);

    // 确保页码范围不会超出总页数
    if (max_page - min_page < pages_in_view - 1) {
        min_page = Math.max(1, max_page - pages_in_view + 1);
    }

    // 清空现有的分页按钮
    const existingPaginationDiv = schedule_info_div.querySelector(".visualization_pagination");
    if (existingPaginationDiv) {
        existingPaginationDiv.remove();
    }

    // 创建页码按钮
    for (let page = min_page; page <= max_page; page++) {
        const page_button = document.createElement("button");
        page_button.innerHTML = page;

        // 添加当前页的样式
        if (page === visualize_current_page) {
            page_button.disabled = true;  // 禁用当前页按钮
            page_button.classList.add("current-page");
        }

        // 点击分页按钮，更新页码并显示对应内容
        page_button.onclick = function () {
            visualize_current_page = page;
            visualize_schedule(generation_int); // 重新显示排课信息
            schedule_info_div.scrollTop = schedule_info_div.scrollHeight;  // 滚动到底部
        };
        
        // 将按钮添加到分页容器
        pagination_div.appendChild(page_button);
    }

    // 添加分页到排课信息显示框
    schedule_info_div.appendChild(pagination_div);
}

// 创建标题单元格（横纵坐标）
function createHeaderCell(content, className) {
    const headerCell = document.createElement("div");
    headerCell.innerText = content;
    headerCell.className = className;
    return headerCell;
}

// 创建不同的颜色样式
function createScheduleCell(course, teacher, conflicts_info_dict) {
    // 创建基础元素
    const cell = document.createElement("div");
    // 指定默认类名
    cell.className = "schedule-cell";
    // 未进行排课的单元格
    if (conflicts_info_dict.is_schedule=='未安排排课')
    {
        cell.classList.add("schedule-cell-not-schedule");
    }
    // 根据情况动态分配样式
    if (conflicts_info_dict.teacher_is_unavailable && conflicts_info_dict.student_is_conflict) {
        cell.classList.add("schedule-cell-multiple-conflicts");
    } 
    else if (conflicts_info_dict.teacher_is_unavailable) {
        cell.classList.add("schedule-cell-unavailable");
    } 
    else if (conflicts_info_dict.student_is_conflict) {
        cell.classList.add("schedule-cell-student-conflict");
    } 
    // 实验课
    if(conflicts_info_dict.schedule_course_type=='实验'){
        // 排课次数超过6次切换显示颜色
        if(conflicts_info_dict.schedule_week_count>4){
            cell.classList.add("schedule_cell_experiment_too_too_many_count");
        }
        // 4（不含）-6（含）次
        // else if(conflicts_info_dict.schedule_week_count>4){
        //     cell.classList.add("schedule_cell_experiment_too_many_count");
        // }
        // 2（含）-4（含）次
        // else if(conflicts_info_dict.schedule_week_count>=2){
        else if(2<=conflicts_info_dict.schedule_week_count && conflicts_info_dict.schedule_week_count<=4){
            cell.classList.add("schedule-cell-experiment");
        }
        // 次数过少
        // else{
        //     cell.classList.add("schedule_cell_experiment_too_less_count");
        // }
    }
    // 理论课
    else {
        // 排课次数超过6次切换显示颜色
        if(conflicts_info_dict.schedule_week_count>3){
            cell.classList.add("schedule_cell_theory_too_too_many_count");
        }
        // 3次
        else if(conflicts_info_dict.schedule_week_count==3){
            cell.classList.add("schedule_cell_theory_too_many_count");
        }
        // 1（含）-2（含）次
        else if(1<=conflicts_info_dict.schedule_week_count && conflicts_info_dict.schedule_week_count<=2){
            // 添加类名
            cell.classList.add("schedule-cell-normal");
        }
        // 次数过少
        // else{
        //     cell.classList.add("schedule_cell_theory_too_less_count");
        // }

    }
    
    // 已排学时和要求学时的距离大于0的标记为橙色
    if(conflicts_info_dict.study_hour_distance_float>0){
        cell.classList.add("schedule-cell-distance_unnormal");
    }

    // 连续排课的标记为棕色
    if(conflicts_info_dict.is_continuous_schedule=='true'){
        cell.classList.add("schedule_cell_continuous");
    }

    // 填充课程和教师信息
    cell.innerHTML = `<strong>${course}</strong><br>${teacher}`;
    return cell;
}

// 创建空单元格
function createEmptyCell() {
    const cell = document.createElement("div");
    cell.className = "schedule-cell schedule-cell-empty";
    return cell;
}

// 下载按钮事件处理
async function download_data_to_excel() {
    // 检查是否有当前选中
    if (cur_generation_int==-1) {
        alert('请先选择一个进化代数');
        return;
    }
    // 有选择,下载内容
    else {
        // window.location.href = `/download_schedule_to_excel?query=${cur_generation_int,cur_fitness_int}`;
        // encodeURIComponent函数，它用于对URI（统一资源标识符）组件进行编码，确保URL中的特殊字符被正确转义
        // window.location.href = `/download_schedule_to_excel?generation=${encodeURIComponent(cur_generation_int)}&fitness=${encodeURIComponent(cur_fitness_float)}`;
        window.location.href = `/download_schedule_to_excel?generation=${cur_generation_int}&fitness=${cur_fitness_float}`;
    }
}