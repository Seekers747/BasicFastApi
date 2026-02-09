// Create User
document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const userData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/users/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();
        const resultDiv = document.getElementById('result');

        if (response.ok) {
            resultDiv.className = 'success';
            resultDiv.textContent = `User created successfully! ID: ${result.id}`;
            document.getElementById('createUserForm').reset();
            loadUsers(); // Refresh the user list
            window.location.replace('/login');
        } else {
            resultDiv.className = 'error';
            resultDiv.textContent = `Error: ${result.detail}`;
        }
    } catch (error) {
        const resultDiv = document.getElementById('result');
        resultDiv.className = 'error';
        resultDiv.textContent = `Error: ${error.message}`;
    }
});

// Login User
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const loginData = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });

        const result = await response.json();
        const resultDiv = document.getElementById('result');

        if (response.ok) {
            resultDiv.className = 'success';
            resultDiv.textContent = `Login successful! Welcome, ${result.username}`;
            window.location.replace('/dashboard');
        } else {
            resultDiv.className = 'error';
            resultDiv.textContent = `Error: ${result.detail}`;
        }
    } catch (error) {
        const resultDiv = document.getElementById('result');
        resultDiv.className = 'error';
        resultDiv.textContent = `Error: ${error.message}`;
    }
});

// Load Users
async function loadUsers() {
    try {
        const response = await fetch('/users/list');
        const users = await response.json();

        const container = document.getElementById('usersContainer');

        if (users.length === 0) {
            container.innerHTML = '<p>No users found.</p>';
            return;
        }

        container.innerHTML = users.map(user => `
            <div class="user-card">
                <strong>ID:</strong> ${user.id}<br>
                <strong>Username:</strong> ${user.username}<br>
                <strong>Email:</strong> ${user.email}<br>
                <button onclick="deleteUser(${user.id})">Delete</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

// Delete User
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) {
        return;
    }

    try {
        const response = await fetch(`/users/delete/${userId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('User deleted successfully!');
            loadUsers();
        } else {
            const result = await response.json();
            alert(`Error: ${result.detail}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Load users when page loads
loadUsers();