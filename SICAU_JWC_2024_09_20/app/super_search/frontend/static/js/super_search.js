let currentPage = 1;
const pageLimit = 10;
let totalPages = 1;
let currentFilter = '';  // 保存当前筛选条件
let currentTable = ''; // 当前选中的表名


// 禁用元素
function disable_element(element_id_str) {
    const element = document.getElementById(element_id_str);
    element.style.pointerEvents = "none";
    element.style.opacity = "0.5";
}

// 启用元素
function enable_element(element_id_str) {
    const element = document.getElementById(element_id_str);
    element.style.pointerEvents = "auto";
    element.style.opacity = "1";
}

// 数据表列查询
async function search_table_js() {
    // 获取输入框的值
    const query = document.getElementById("search_table_input").value;
    if (!query.trim()) {
        return;
    }
    
    // 重置筛选框和筛选条件
    resetFilter();
    // 禁用三个输入框和按钮
    disable_element("search_table_div");
    disable_element('search_database_div');
    disable_element('search_filter_div');

    const response = await fetch(`/search?query=${query}`);
    const data = await response.json();

    const resultsDiv = document.getElementById("table_match_content_div");
    resultsDiv.innerHTML = "";

    Object.keys(data.tables).forEach(tableName => {
        const tableDiv = document.createElement("div");
        tableDiv.innerHTML = `<strong>${tableName}:</strong>`;

        const columns = data.tables[tableName];
        if (columns.length > 0) {
            tableDiv.innerHTML += ` ${columns.join(", ")}`;
        }

        tableDiv.onclick = () => loadTableData(tableName,1,true);
        resultsDiv.appendChild(tableDiv);
    });

    // 启用三个输入框和按钮
    enable_element("search_table_div");
    enable_element('search_database_div');
    enable_element('search_filter_div');

}
        
// 全数据库查询
async function search_database_js() {
    
    // 获取输入框的值
    const search_keyword = document.getElementById("search_database_input").value;
    if (!search_keyword.trim()) {
        return;
    }

    // 重置筛选框和筛选条件
    resetFilter();

    // 禁用三个输入框和内部按钮
    disable_element("search_table_div");
    disable_element('search_database_div');
    disable_element('search_filter_div');
    
    const resultsDiv = document.getElementById("database_match_content_div");
    // 锁定 resultsDiv，禁用用户交互
    disable_element('database_match_content_div');
    // 清空之前的结果
    resultsDiv.innerHTML = "";


    // 建立WebSocket连接
    const ws = new WebSocket('/ws_search_database');
    // WebSocket 打开后发送搜索关键词
    ws.onopen = function() {
        ws.send(search_keyword);
    };

    // 实时显示查询进度
    ws.onmessage = function(event) {

        // 检查是否是搜索完成标志
        if (event.data === 'search_done') {
            // 等待接收到排序后的完整数据,用新接收的数据重新渲染页面数据
            ws.onmessage = function(event) {
                // 解析接收到的 JSON 数据
                const response_data = JSON.parse(event.data);
                const tables = response_data.tables;
                
                // 清空之前显示的实时结果
                resultsDiv.innerHTML = "";

                Object.keys(tables).forEach(tableName => {
                    // 创建一个新的 div 来显示新的一行信息
                    const tableDiv = document.createElement("div");
                    tableDiv.innerHTML = `<strong>${tableName}:</strong>`;

                    const columns = tables[tableName];
                    Object.keys(columns).forEach(columnName => {
                        const columnContent = columns[columnName];
                        // 列内容换行
                        tableDiv.innerHTML += `${columnName}<br>`;
                        tableDiv.innerHTML += `${columnContent}<br>`;
                    });
                    // 绑定点击事件
                    tableDiv.onclick = () => loadTableData(tableName, 1, true);
                    resultsDiv.appendChild(tableDiv);
                });
                // 更新滚动条滚动到最顶上位置
                resultsDiv.scrollTop = 0;
                
                // 解锁 resultsDiv
                enable_element('database_match_content_div')
                // 启用三个输入框和按钮
                enable_element("search_table_div");
                enable_element('search_database_div');
                enable_element('search_filter_div');
                // 关闭 WebSocket 连接
                // ws.close();
            }
        }
        else {
            // 显示实时结果
            const response_data = JSON.parse(event.data);
            // 提取发送过来的字段
            const table_name_str = response_data.table_name;
            const column_str = response_data.column;
            const content_str = response_data.content;

            // 创建一个新的 div 来显示新的一行信息
            const tableDiv = document.createElement("div");
            // 显示消息
            // resultsDiv.innerHTML += `<p>${event.data}</p>`;
            tableDiv.innerHTML = `<span><strong>表名:</strong> ${table_name_str}</span> `;
            tableDiv.innerHTML += `<span><strong>列名:</strong> ${column_str}</span> <br>`;
            tableDiv.innerHTML += `<span><strong>相关内容:</strong> ${content_str}</span> <br>`;

            resultsDiv.appendChild(tableDiv);
            // 更新滚动条到底端位置,以显示最新的信息
            resultsDiv.scrollTop = resultsDiv.scrollHeight;
        }
    }

}

// 设置当前筛选条件并加载数据
function search_filter_js() {
    const filterInput = document.getElementById("search_filter_input").value.trim();
    currentFilter = filterInput;  // 更新当前筛选条件

    // 禁用三个输入框和按钮
    disable_element("search_table_div");
    disable_element('search_database_div');
    disable_element('search_filter_div');
    
    if (currentTable) {
        loadTableData(currentTable, 1, false);  // 使用当前筛选条件重新加载表数据，不重置筛选框
    }
    // 启用三个输入框和按钮
    enable_element("search_table_div");
    enable_element('search_database_div');
    enable_element('search_filter_div');
}

// 修改 loadTableData 函数，使其支持筛选条件
async function loadTableData(tableName, page,shouldResetFilter = false) {
    // 重置筛选框和筛选条件
    // 根据shouldResetFilter判断是否重置筛选条件
    if (shouldResetFilter) {
        resetFilter();  // 仅在点击表名或查询时重置筛选框
    }

    currentPage = page;  // 设置当前页
    currentTable = tableName;  // 更新当前选中的表名
    const filterValue = currentFilter;  // 获取当前的筛选条件

    const response = await fetch(`/table/${tableName}/data?page=${page}&limit=${pageLimit}&filter=${filterValue}`);
    const data = await response.json();
    const tableDiv = document.getElementById("table_data_div");
    tableDiv.innerHTML = `<h3>表内容: ${data.table_name}</h3>`;

    if (data.data.length === 0) {
        tableDiv.innerHTML = "<p>没有数据</p>";  // 显示没有数据
        totalPages = 1;
        renderPagination(tableName);
        return;
    }

    const table = document.createElement("table");
    const headerRow = document.createElement("tr");

    // 添加表头
    Object.keys(data.data[0]).forEach(col => {
        const th = document.createElement("th");
        th.innerText = col;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // 填充表格内容
    data.data.forEach(row => {
        const tr = document.createElement("tr");
        Object.values(row).forEach(value => {
            const td = document.createElement("td");
            td.innerText = value;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });

    tableDiv.appendChild(table);
        totalPages = data.total_pages;  // 更新总页数

    // 渲染分页按钮
    renderPagination(tableName);
}

// 渲染分页
function renderPagination(tableName) {
    const paginationDiv = document.createElement("div");
    paginationDiv.className = "pagination";
    paginationDiv.innerHTML = "";

    const prevButton = document.createElement("button");
    prevButton.innerText = "上一页";
    prevButton.disabled = currentPage === 1;
    prevButton.onclick = () => {
        if (currentPage > 1) {
            loadTableData(tableName, currentPage - 1);
        }
    };
    paginationDiv.appendChild(prevButton);

    const halfRange = 5;
    let start = Math.max(1, currentPage - halfRange);
    let end = Math.min(totalPages, currentPage + halfRange);

    if (end - start < 9) {
        start = Math.max(1, end - 9);
        }

    for (let i = start; i <= end; i++) {
        const button = document.createElement("button");
        button.innerText = i;
        button.onclick = () => {
            loadTableData(tableName, i);
        };
        if (i === currentPage) {
            button.classList.add("current-page");  // 添加当前页的样式
        }
        paginationDiv.appendChild(button);
    }

    const nextButton = document.createElement("button");
    nextButton.innerText = "下一页";
    nextButton.disabled = currentPage === totalPages;
    nextButton.onclick = () => {
        if (currentPage < totalPages) {
            loadTableData(tableName, currentPage + 1);
        }
    };
    paginationDiv.appendChild(nextButton);

    // 确保只追加一次分页栏，清空之前的内容
    const tableDiv = document.getElementById("table_data_div");
    const existingPagination = tableDiv.querySelector(".pagination");
    if (existingPagination) {
        tableDiv.removeChild(existingPagination);
    }
    tableDiv.appendChild(paginationDiv);
}

// 重置筛选框和筛选条件
function resetFilter() {
    document.getElementById("search_filter_input").value = "";  // 清空筛选框
    currentFilter = "";  // 重置筛选条件
}

// 下载按钮事件处理
async function download_data_to_excel() {
    // 检查是否有当前选中的表
    if (!currentTable) {
        alert('请先选择一个表');
        return;
    }
    // 有选择的表,下载此表的内容
    else {
        window.location.href = `/download_excel/${currentTable}?filter=${encodeURIComponent(currentFilter)}`;
    }
}