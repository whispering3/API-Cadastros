const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:') 
    ? 'http://localhost:8000/api/v1' 
    : '/api/v1';
let authToken = localStorage.getItem('token');
let currentUser = null;
let currentOrderFilter = 'me'; // 'all', 'me' ou ID do usuário

document.addEventListener('DOMContentLoaded', async () => {
    if (authToken) {
        try {
            const userRes = await fetch(`${API_BASE}/users/me`, {
                headers: { 'Authorization': `Bearer ${authToken}` }
            });
            if (userRes.ok) {
                currentUser = await userRes.json();
                showDashboard();
            } else {
                logout();
            }
        } catch (err) {
            logout();
        }
    }

    // Máscara de CPF em tempo real
    const cpfInput = document.getElementById('reg-cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 11) v = v.slice(0, 11);
            if (v.length > 9) v = v.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, "$1.$2.$3-$4");
            else if (v.length > 6) v = v.replace(/^(\d{3})(\d{3})(\d{1,3})$/, "$1.$2.$3");
            else if (v.length > 3) v = v.replace(/^(\d{3})(\d{1,3})$/, "$1.$2");
            e.target.value = v;
        });
    }
});

// Navegação
function toggleAuthTab(tab) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        tabLogin.classList.remove('active');
        tabRegister.classList.add('active');
    }
}

function showSection(section) {
    document.getElementById('users-section').classList.add('hidden');
    document.getElementById('orders-section').classList.add('hidden');
    document.getElementById(`${section}-section`).classList.remove('hidden');

    if (section === 'users') loadUsers();
    if (section === 'orders') {
        loadOrders();
        populateOrderFilter();
    }
}

async function populateOrderFilter() {
    try {
        const response = await fetch(`${API_BASE}/users/`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const users = await response.json();
        const select = document.getElementById('filter-user-id');
        
        // Mantém as opções fixas e adiciona os usuários
        select.innerHTML = `
            <option value="all">Todos os Usuários</option>
            <option value="me">Meus Pedidos</option>
        `;
        
        users.forEach(u => {
            if (currentUser && u.id !== currentUser.id) {
                const opt = document.createElement('option');
                opt.value = u.id;
                opt.innerText = `${u.nome} (ID: ${u.id})`;
                select.appendChild(opt);
            }
        });
    } catch (err) {
        console.error('Erro ao popular filtro', err);
    }
}

async function loadOrdersByFilter() {
    const val = document.getElementById('filter-user-id').value;
    currentOrderFilter = val; // Memoriza o filtro atual
    
    if (val === 'all') loadOrders(true);
    else if (val === 'me') loadOrders(false);
    else {
        try {
            const response = await fetch(`${API_BASE}/orders/?user_id=${val}`, {
                headers: { 'Authorization': `Bearer ${authToken}` }
            });
            const orders = await response.json();
            renderOrders(orders);
        } catch (err) {
            showToast('Erro ao filtrar pedidos', 'error');
        }
    }
}

// Auth
async function handleLogin() {
    const email = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw await response.json();

        const data = await response.json();
        authToken = data.access_token;
        localStorage.setItem('token', authToken);
        
        // Busca info do usuário logado
        const userRes = await fetch(`${API_BASE}/users/me`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        currentUser = await userRes.json();
        
        showToast('Login realizado com sucesso!', 'success');
        showDashboard();
    } catch (err) {
        showToast(err.detail || 'Falha no login', 'error');
    }
}

async function handleRegister() {
    const data = {
        nome: document.getElementById('reg-nome').value,
        email: document.getElementById('reg-email').value,
        login: document.getElementById('reg-login').value,
        cpf: document.getElementById('reg-cpf').value,
        rg: document.getElementById('reg-rg').value,
        idade: parseInt(document.getElementById('reg-idade').value),
        password: document.getElementById('reg-password').value
    };

    try {
        const response = await fetch(`${API_BASE}/users/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw await response.json();

        showToast('Cadastro realizado! Faça login.', 'success');
        toggleAuthTab('login');
    } catch (err) {
        showToast(err.detail || 'Falha no cadastro', 'error');
    }
}

function logout() {
    localStorage.removeItem('token');
    authToken = null;
    location.reload();
}

function showDashboard() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('main-nav').classList.remove('hidden');
    showSection('users');
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE}/users/`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const users = await response.json();
        const list = document.getElementById('users-list');
        list.innerHTML = '';

        users.forEach(user => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${user.id}</td>
                <td>${user.nome}</td>
                <td>${user.email}</td>
                <td>${user.cpf}</td>
                <td><span class="badge badge-success">Ativo</span></td>
                <td class="actions">
                    <button class="btn-edit" onclick="editUser(${user.id})">Editar</button>
                    <button class="btn-delete" onclick="deleteUser(${user.id})">Excluir</button>
                </td>
            `;
            list.appendChild(tr);
        });
    } catch (err) {
        showToast('Falha ao carregar usuários', 'error');
    }
}

async function loadOrders(all = false) {
    try {
        let url = `${API_BASE}/orders/`;
        if (!all && currentUser) {
            url += `?user_id=${currentUser.id}`;
        }

        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const orders = await response.json();
        renderOrders(orders);
    } catch (err) {
        showToast('Falha ao carregar pedidos', 'error');
    }
}

function renderOrders(orders) {
    const list = document.getElementById('orders-list');
    list.innerHTML = '';

    orders.forEach(order => {
        const div = document.createElement('div');
        div.className = 'order-card fade-in';
        div.innerHTML = `
            <div class="order-header">
                <h3>Pedido #${order.id}</h3>
                <div class="actions">
                    <button class="btn-edit" onclick="editOrder(${order.id}, '${order.descricao}')">Editar</button>
                    <button class="btn-delete" onclick="deleteOrderApi(${order.id})">Excluir</button>
                </div>
            </div>
            <p><strong>Usuário:</strong> ${order.user_nome} (ID: ${order.user_id})</p>
            <p><strong>Descrição:</strong> ${order.descricao}</p>
            <div class="date">${new Date(order.created_at).toLocaleString()}</div>
        `;
        list.appendChild(div);
    });
}

// Ações
async function editUser(id) {
    try {
        const response = await fetch(`${API_BASE}/users/`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const users = await response.json();
        const user = users.find(u => u.id === id);
        
        const content = `
            <h2>Editar Usuário #${id}</h2>
            <div class="grid">
                <div class="input-group"><label>Nome</label><input type="text" id="edit-nome" value="${user.nome}"></div>
                <div class="input-group"><label>Email</label><input type="email" id="edit-email" value="${user.email}"></div>
                <div class="input-group"><label>Login</label><input type="text" id="edit-login" value="${user.login}"></div>
                <div class="input-group"><label>RG</label><input type="text" id="edit-rg" value="${user.rg || ''}"></div>
                <div class="input-group"><label>Idade</label><input type="number" id="edit-idade" value="${user.idade || ''}"></div>
                <div class="input-group"><label>Nova Senha (opcional)</label><input type="password" id="edit-password"></div>
            </div>
            <button class="btn-primary" onclick="updateUserData(${id})">Salvar Alterações</button>
        `;
        openModal(content);
    } catch (err) {
        showToast('Erro ao carregar dados do usuário', 'error');
    }
}

async function updateUserData(id) {
    const data = {
        nome: document.getElementById('edit-nome').value,
        email: document.getElementById('edit-email').value,
        login: document.getElementById('edit-login').value,
        rg: document.getElementById('edit-rg').value,
        idade: parseInt(document.getElementById('edit-idade').value) || null
    };
    
    const pwd = document.getElementById('edit-password').value;
    if (pwd) data.password = pwd;

    try {
        const response = await fetch(`${API_BASE}/users/${id}`, {
            method: 'PATCH',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}` 
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            showToast('Usuário atualizado!', 'success');
            closeModal();
            loadUsers();
        } else {
            const err = await response.json();
            showToast(err.detail, 'error');
        }
    } catch (err) {
        showToast('Erro ao atualizar', 'error');
    }
}

async function deleteUser(id) {
    const physical = confirm('Deseja exclusão física (OK) ou lógica (Cancelar)?');
    try {
        const response = await fetch(`${API_BASE}/users/${id}?physical=${physical}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            showToast('Usuário removido', 'success');
            loadUsers();
        }
    } catch (err) {
        showToast('Erro ao excluir', 'error');
    }
}

function showNewOrderModal() {
    const content = `
        <h2>Novo Pedido</h2>
        <div class="input-group">
            <label>Descrição do Pedido <span style="color: var(--danger)">*</span></label>
            <input type="text" id="order-desc" placeholder="Ex: Headset Gamer">
        </div>
        <button class="btn-primary" onclick="createOrder()">Criar Pedido</button>
    `;
    openModal(content);
}

async function createOrder() {
    const desc = document.getElementById('order-desc').value;
    
    if (!desc.trim()) {
        showToast('A descrição do pedido é obrigatória!', 'error');
        document.getElementById('order-desc').focus();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/orders/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ descricao: desc })
        });
        if (response.ok) {
            showToast('Pedido criado!', 'success');
            closeModal();
            loadOrdersByFilter();
        }
    } catch (err) {
        showToast('Erro ao criar pedido', 'error');
    }
}

async function editOrder(id, currentDesc) {
    const content = `
        <h2>Editar Pedido #${id}</h2>
        <div class="input-group">
            <label>Nova Descrição</label>
            <input type="text" id="edit-order-desc" value="${currentDesc}">
        </div>
        <button class="btn-primary" onclick="updateOrderData(${id})">Salvar</button>
    `;
    openModal(content);
}

async function updateOrderData(id) {
    const desc = document.getElementById('edit-order-desc').value;
    try {
        const response = await fetch(`${API_BASE}/orders/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ descricao: desc })
        });
        if (response.ok) {
            showToast('Pedido atualizado!', 'success');
            closeModal();
            loadOrdersByFilter();
        }
    } catch (err) {
        showToast('Erro ao atualizar pedido', 'error');
    }
}

async function deleteOrderApi(id) {
    if (!confirm('Deseja excluir este pedido?')) return;
    try {
        const response = await fetch(`${API_BASE}/orders/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            showToast('Pedido removido', 'success');
            loadOrdersByFilter(); // Recarrega usando o filtro memorizado
        }
    } catch (err) {
        showToast('Erro ao excluir pedido', 'error');
    }
}

// UI Componentes
function openModal(html) {
    document.getElementById('modal-content').innerHTML = html;
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
}

function showToast(msg, type) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    // Se a mensagem for um array (erro do FastAPI), formata para string
    let message = msg;
    if (Array.isArray(msg)) {
        message = msg.map(err => `${err.loc[1]}: ${err.msg}`).join(' | ');
    } else if (typeof msg === 'object' && msg !== null) {
        message = JSON.stringify(msg);
    }
    
    toast.innerText = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}
