document.addEventListener('DOMContentLoaded', function() {
  console.log('Scripts loaded successfully!');

  // ===== Dark Mode Toggle =====
  const body = document.body;
  // Check localStorage for saved dark mode preference
  if (localStorage.getItem('darkMode') === 'enabled') {
    body.classList.add('dark-mode');
  }

  const darkModeToggle = document.getElementById('darkModeToggle');
  if (darkModeToggle) {
    darkModeToggle.addEventListener('click', function() {
      body.classList.toggle('dark-mode');
      if (body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
      } else {
        localStorage.setItem('darkMode', 'disabled');
      }
    });
  }

  // ===== Drag-and-Drop Sorting =====
  const taskList = document.getElementById('task-list'); // Ensure your HTML element has this ID
  if (taskList) {
    new Sortable(taskList, {
      animation: 150,
      ghostClass: 'sortable-ghost'
    });
  }

  // ===== Delete Confirmation =====
  const deleteForms = document.querySelectorAll('.delete-form');
  deleteForms.forEach(function(form) {
    form.addEventListener('submit', function(event) {
      if (!confirm('Are you sure you want to delete this task?')) {
        event.preventDefault();
      }
    });
  });
});