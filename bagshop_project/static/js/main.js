// === Получение CSRF-токена ===
function getCsrfToken() {
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));
  return cookie ? cookie.split("=")[1] : "";
}

// === Универсальный fetch с авторизацией ===
async function apiRequest(url, options = {}) {
  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    credentials: "include",
  };

  const finalOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, finalOptions);

    if (response.status === 401 || response.status === 403) {
      showNotification(
        "Необходима авторизация. Перенаправляем на вход...",
        "warning",
      );
      setTimeout(() => (window.location.href = "/login/"), 2000);
      throw new Error("Unauthorized");
    }

    return response;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// === Загрузка товаров (ТОЛЬКО для страниц, где нужна динамическая загрузка) ===
async function loadProducts() {
  const grid = document.getElementById("product-grid");
  if (!grid) return;

  // Проверяем, есть ли на странице атрибут data-dynamic
  const container = document.getElementById("product-grid");
  if (container && container.dataset.dynamic !== "true") {
    // Если динамическая загрузка не включена — выходим
    console.log("Динамическая загрузка отключена для этой страницы");
    return;
  }

  grid.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
            <p class="mt-3">Загрузка товаров...</p>
        </div>
    `;

  try {
    const response = await apiRequest("/api/products/");
    const products = await response.json();

    if (products.length === 0) {
      grid.innerHTML = `<p class="text-center">Товары не найдены</p>`;
      return;
    }

    grid.innerHTML = products
      .map(
        (product) => `
            <div class="col-sm-6 col-md-4 col-lg-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <img src="${product.product_img || "https://via.placeholder.com/300x200"}" 
                         class="card-img-top" alt="${product.name}" 
                         style="height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h6 class="card-title">${product.name.substring(0, 30)}</h6>
                        <p class="card-text text-primary fw-bold">${product.price} руб.</p>
                        <a href="/catalog/${product.id}/" class="btn btn-outline-primary btn-sm w-100">Подробнее</a>
                    </div>
                </div>
            </div>
        `,
      )
      .join("");
  } catch (error) {
    grid.innerHTML = `
            <div class="alert alert-danger text-center">
                <i class="fas fa-exclamation-triangle"></i> 
                Ошибка загрузки товаров: ${error.message}
            </div>
        `;
  }
}

// === Добавление в корзину ===
async function addToCart(productId) {
  try {
    const response = await apiRequest(`/api/carts/add/${productId}/`, {
      method: "POST",
    });

    if (response.ok) {
      showNotification("Товар добавлен в корзину!", "success");
    } else {
      const error = await response.json();
      showNotification(error.detail || "Ошибка добавления в корзину", "danger");
    }
  } catch (error) {
    showNotification(error.message, "danger");
  }
}

// === Уведомления ===
function showNotification(message, type = "success") {
  const container = document.querySelector(".container");
  if (!container) return;

  const alert = document.createElement("div");
  alert.className = `alert alert-${type} alert-dismissible fade show`;
  alert.role = "alert";
  alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  container.prepend(alert);
  setTimeout(() => alert.remove(), 5000);
}

// === Обновление счётчика корзины ===
async function updateCartCount() {
  try {
    const response = await fetch("/api/carts/my_cart/");
    if (!response.ok) return;
    const cart = await response.json();
    const count = cart.items?.length || 0;
    const badge = document.querySelector(".cart-badge");
    if (badge) badge.textContent = count;
  } catch (e) {
    // Игнорируем
  }
}

// === Запуск ===
document.addEventListener("DOMContentLoaded", () => {
  // Загружаем товары только если есть элемент и включена динамическая загрузка
  const grid = document.getElementById("product-grid");
  if (grid && grid.dataset.dynamic === "true") {
    loadProducts();
  }
  updateCartCount();
});
