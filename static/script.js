document.addEventListener('DOMContentLoaded', () => {
  // Helper function to set up event listeners
  function addEventListenerToElements(elements, event, callback) {
    elements.forEach(element => {
      element.addEventListener(event, callback);
    });
  }

  // Navbar burger toggle functionality
  function setupNavbarBurger() {
    const navbarBurgers = Array.from(document.querySelectorAll('.navbar-burger'));
    addEventListenerToElements(navbarBurgers, 'click', function() {
      const target = this.dataset.target;
      const targetElement = document.getElementById(target);
      this.classList.toggle('is-active');
      targetElement.classList.toggle('is-active');
    });
  }

  // Love button functionality
  function setupLoveButtons() {
    const loveButtons = document.querySelectorAll('.love-button');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    addEventListenerToElements(loveButtons, 'click', function() {
      const postId = this.id.split('-')[2];

      fetch(`/post/${postId}/love/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'post_id': postId })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          this.textContent = data.loved ? '❤️' : '🤍';
          document.getElementById(`love-count-${postId}`).textContent = data.new_love_count;
        } else {
          console.error('Failed to update love status');
        }
      })
      .catch(err => console.error('Fetch error:', err));
    });
  }

  // Form submission handler
  function setupFormSubmitHandler(formId, apiUrl, successMessage = 'Operation successful') {
    const form = document.getElementById(formId);

    if (form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(apiUrl, {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          alert(data.message || successMessage);
          // Optionally, redirect or update the UI after success
        })
        .catch(error => {
          console.error('Error:', error);
        });
      });
    }
  }

  // Initial setup
  setupNavbarBurger();
  setupLoveButtons();
  setupFormSubmitHandler('signupForm', '/api/signup/', 'Signup successful');
  setupFormSubmitHandler('loginForm', '/api/login/', 'Login successful');
  setupFormSubmitHandler('logoutButton', '/api/logout/', 'Logout successful');
});
