function filterTable(inp, tbl) {
  const v = document.getElementById(inp).value.toUpperCase();
  const rows = document.getElementById(tbl).rows;
  for (let i = 1; i < rows.length; i++) {
    rows[i].style.display = Array.from(rows[i].cells)
      .some(td => td.textContent.toUpperCase().includes(v)) ? '' : 'none';
  }
}
function toggleForm(id) {
  const f = document.getElementById(id);
  f.classList.toggle('hidden');
}
function validateStaffForm() {
  const f = document.getElementById('staffForm');
  if (!f.name.value || !f.position.value || !f.email.value) {
    alert('Please fill all staff fields'); return false;
  }
  alert('Staff saved (demo)');
  f.reset(); toggleForm('staffForm');
  return false;
}
function validateManagerForm() {
  const f = document.getElementById('managerForm');
  if (!f.name.value || !f.department.value || !f.email.value) {
    alert('Fill all fields'); return false;
  }
  alert('Manager saved (demo)');
  f.reset(); toggleForm('managerForm');
  return false;
}
function validateCategoryForm() {
  const f = document.getElementById('categoryForm');
  if (!f.name.value || !f.desc.value) {
    alert('Fill all'); return false;
  }
  alert('Category saved');
  f.reset(); toggleForm('categoryForm');
  return false;
}
function validateProductForm() {
  const f = document.getElementById('productsForm');
  if (!f.name.value || !f.category.value || !f.price.value || !f.qty.value) {
    alert('Fill all'); return false;
  }
  alert('Product saved');
  f.reset(); toggleForm('productsForm');
  return false;
}
function validateCustomerForm() {
  const f = document.getElementById('customersForm');
  if (!f.name.value || !f.phone.value || !f.email.value) {
    alert('Fill all'); return false;
  }
  alert('Customer saved');
  f.reset(); toggleForm('customersForm');
  return false;
}
// Helper function to fetch data from API
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
}

// Helper function to post data to API
async function postData(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Failed to save data');
        }
        return result;
    } catch (error) {
        console.error('Error posting data:', error);
        alert(`Error: ${error.message}`);
        return null;
    }
}

// Function to populate tables from backend
async function populateTable(apiEndpoint, tableId, headers, rowMapper) {
    const table = document.getElementById(tableId);
    if (!table) return; // Exit if table doesn't exist on the current page

    // Clear existing rows (except header)
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    const data = await fetchData(apiEndpoint);
    data.forEach(item => {
        const row = table.insertRow();
        rowMapper(row, item); // Use a mapper function to populate cells
    });
}

// Specific table population functions
async function populateCategoriesTable() {
    const headers = ['Name', 'Description'];
    const rowMapper = (row, item) => {
        row.insertCell().textContent = item.name;
        row.insertCell().textContent = item.description;
    };
    await populateTable('/api/categories', 'categoryTable', headers, rowMapper);
}

async function populateProductsTable() {
    const headers = ['Name', 'Category', 'Price', 'Qty'];
    const rowMapper = (row, item) => {
        row.insertCell().textContent = item.name;
        row.insertCell().textContent = item.category_name; // Use category_name from join
        row.insertCell().textContent = `₹${item.price}`;
        row.insertCell().textContent = item.quantity;
    };
    await populateTable('/api/products', 'productsTable', headers, rowMapper);
}

async function populateStaffTable() {
    const headers = ['Name', 'Position', 'Email'];
    const rowMapper = (row, item) => {
        row.insertCell().textContent = item.name;
        row.insertCell().textContent = item.position;
        row.insertCell().textContent = item.email;
    };
    await populateTable('/api/staff', 'staffTable', headers, rowMapper);
}

async function populateManagersTable() {
    const headers = ['Name', 'Department', 'Email'];
    const rowMapper = (row, item) => {
        row.insertCell().textContent = item.name;
        row.insertCell().textContent = item.department;
        row.insertCell().textContent = item.email;
    };
    await populateTable('/api/managers', 'managerTable', headers, rowMapper);
}

async function populateCustomersTable() {
    const headers = ['Name', 'Phone', 'Email'];
    const rowMapper = (row, item) => {
        row.insertCell().textContent = item.name;
        row.insertCell().textContent = item.phone;
        row.insertCell().textContent = item.email;
    };
    await populateTable('/api/customers', 'customersTable', headers, rowMapper);
}


// Call populate functions on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check which page is loaded and call the appropriate populate function
    if (document.getElementById('categoryTable')) {
        populateCategoriesTable();
    }
    if (document.getElementById('productsTable')) {
        populateProductsTable();
    }
    if (document.getElementById('staffTable')) {
        populateStaffTable();
    }
    if (document.getElementById('managerTable')) {
        populateManagersTable();
    }
    if (document.getElementById('customersTable')) {
        populateCustomersTable();
    }
});


// Existing filterTable and toggleForm functions (no changes needed)
function filterTable(inp, tbl) {
    const v = document.getElementById(inp).value.toUpperCase();
    const rows = document.getElementById(tbl).rows;
    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = Array.from(rows[i].cells)
            .some(td => td.textContent.toUpperCase().includes(v)) ? '' : 'none';
    }
}

function toggleForm(id) {
    const f = document.getElementById(id);
    f.classList.toggle('hidden');
}

// Modified validation and submission functions to use API
async function validateStaffForm() {
    const f = document.getElementById('staffForm');
    const name = f.name.value;
    const position = f.position.value;
    const email = f.email.value;

    if (!name || !position || !email) {
        alert('Please fill all staff fields');
        return false;
    }

    const result = await postData('/api/staff', { name, position, email });
    if (result) {
        alert('Staff saved successfully!');
        f.reset();
        toggleForm('staffForm');
        populateStaffTable(); // Refresh table
    }
    return false; // Prevent default form submission
}

async function validateManagerForm() {
    const f = document.getElementById('managerForm');
    const name = f.name.value;
    const department = f.department.value;
    const email = f.email.value;

    if (!name || !department || !email) {
        alert('Fill all fields');
        return false;
    }

    const result = await postData('/api/managers', { name, department, email });
    if (result) {
        alert('Manager saved successfully!');
        f.reset();
        toggleForm('managerForm');
        populateManagersTable(); // Refresh table
    }
    return false;
}

async function validateCategoryForm() {
    const f = document.getElementById('categoryForm');
    const name = f.name.value;
    const description = f.desc.value;

    if (!name || !description) {
        alert('Fill all fields');
        return false;
    }

    const result = await postData('/api/categories', { name, description });
    if (result) {
        alert('Category saved successfully!');
        f.reset();
        toggleForm('categoryForm');
        populateCategoriesTable(); // Refresh table
    }
    return false;
}

async function validateProductForm() {
    const f = document.getElementById('productsForm');
    const name = f.name.value;
    const category = f.category.value;
    const price = parseFloat(f.price.value);
    const qty = parseInt(f.qty.value);

    if (!name || !category || isNaN(price) || isNaN(qty)) {
        alert('Fill all fields correctly');
        return false;
    }

    const result = await postData('/api/products', { name, category, price, qty });
    if (result) {
        alert('Product saved successfully!');
        f.reset();
        toggleForm('productsForm');
        populateProductsTable(); // Refresh table
    }
    return false;
}

async function validateCustomerForm() {
    const f = document.getElementById('customersForm');
    const name = f.name.value;
    const phone = f.phone.value;
    const email = f.email.value;

    if (!name || !phone || !email) {
        alert('Fill all fields');
        return false;
    }

    const result = await postData('/api/customers', { name, phone, email });
    if (result) {
        alert('Customer saved successfully!');
        f.reset();
        toggleForm('customersForm');
        populateCustomersTable(); // Refresh table
    }
    return false;
}
