document.addEventListener('DOMContentLoaded', function() {
    const deleteBtn = document.getElementById('deleteBtn');
    const taskForm = document.getElementById('taskForm');
    const popup = document.getElementById('popup');

    // Add event listener for deleting completed tasks (if not already added)

    if (deleteBtn) {
        deleteBtn.addEventListener('click', function(event) {
            event.preventDefault();
            if (confirm("Are you sure you want to delete completed tasks?")) {
                fetch("/delete_completed_tasks", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }
                })
                .then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        throw new Error('Network response was not ok.');
                    }
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
            }
        });
    }

    // Add event listener for submitting tasks (if not already added)

    if (taskForm) {
        taskForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(taskForm);
            const task = formData.get('task');
            const dueDate = formData.get('due_date');
            const category = formData.get('category');

            taskForm.classList.add('submitting');
            const spinner = taskForm.querySelector('.spinner');
            spinner.style.display = 'inline-block';

            fetch("/add_task", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ task, dueDate, category })
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            })
            .finally(() => {
                taskForm.classList.remove('submitting');
                spinner.style.display = 'none';
            });
        });
    }

    // Add additional JavaScript functionalities as needed
});
