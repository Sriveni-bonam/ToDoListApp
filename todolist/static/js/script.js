document.addEventListener("DOMContentLoaded", function () {
    updateProgressBar();
    updateTaskCounts();
});

// Update progress bar
function updateProgressBar() {
    let tasks = document.querySelectorAll(".task-item");
    let completedTasks = document.querySelectorAll(".task-item.completed");
    
    let percentage = tasks.length === 0 ? 0 : (completedTasks.length / tasks.length) * 100;
    document.getElementById("task-progress").style.width = percentage + "%";
}

// Toggle view between Add Task and Task List
function toggleView(view) {
    const addTaskView = document.getElementById('add-task-view');
    const taskListView = document.getElementById('task-list-view');
    const searchBar = document.getElementById('search-bar');

    if (view === 'add-task') {
        addTaskView.classList.remove('hidden');
        taskListView.classList.add('hidden');
        searchBar.style.display = 'none'; // Hide the search bar
    } else if (view === 'task-list') {
        addTaskView.classList.add('hidden');
        taskListView.classList.remove('hidden');
        searchBar.style.display = 'block'; // Show the search bar
    }
}

// Function to filter tasks based on selected filters
function filterTasks() {
    const priorityFilter = document.getElementById('priority-filter').value;
    const categoryFilter = document.getElementById('category-filter').value;

    const tasks = document.querySelectorAll('.task-item');
    tasks.forEach(function(task) {
        const taskPriority = task.querySelector('.task-priority').textContent.trim();
        const taskCategoryId = task.getAttribute('data-category-id'); 
        let showTask = true;

        if (priorityFilter && taskPriority !== priorityFilter) {
            showTask = false;
        }
        if (categoryFilter && taskCategoryId !== categoryFilter) {
            showTask = false;
        }

        task.style.display = showTask ? 'block' : 'none';
    });

    updateTaskCounts();
}

// Function to remove all applied filters
function removeFilters() {
    document.getElementById('priority-filter').value = '';
    document.getElementById('category-filter').value = '';
    filterTasks();
}

// Function to update the counts of pending and completed tasks
function updateTaskCounts() {
    const tasks = document.querySelectorAll('.task-item');
    let pendingCount = 0;
    let completedCount = 0;

    tasks.forEach(task => {
        if (task.style.display !== 'none') {
            const taskStatus = task.getAttribute('data-status');
            if (taskStatus === 'True') {
                completedCount++;
            } else {
                pendingCount++;
            }
        }
    });

    document.getElementById('pending-count').textContent = 'Pending: ' + pendingCount;
    document.getElementById('completed-count').textContent = 'Completed: ' + completedCount;
}

// Function to search tasks based on title
function searchTasks() {
    const searchQuery = document.getElementById('search-input').value.toLowerCase();
    const tasks = document.querySelectorAll('.task-item');

    tasks.forEach(task => {
        const taskTitle = task.querySelector('.task-title').textContent.toLowerCase();
        task.style.display = taskTitle.includes(searchQuery) ? 'block' : 'none';
    });

    updateTaskCounts();
}
