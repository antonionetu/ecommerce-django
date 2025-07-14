document.addEventListener("DOMContentLoaded", function () {
    let isLoading = false;
    let currentPage = 1;
    let notFound = false;

    window.addEventListener("scroll", function () {
        const scrollTop = window.scrollY;
        const windowHeight = window.innerHeight;
        const docHeight = document.documentElement.scrollHeight;
        const isAtBellow = scrollTop + windowHeight >= docHeight - 100;

        if (!isLoading && isAtBellow && !notFound) {
            isLoading = true;
            currentPage += 1;

            fetchProducts(currentPage)
                .then(products => {
                    renderProducts(products);
                })
                .catch(error => {
                    console.error("Erro ao carregar mais produtos:", error);
                    notFound = true
                    currentPage -= 1;
                })
                .finally(() => {
                    isLoading = false;
                });
        }
    });
});

function fetchProducts(page) {
    return fetch(`${getProductsUrl}?p=${page}`)
        .then(response => {
            if (response.status !== 200) {
                throw new Error("Produtos não encontrados");
            }
            return response.json();
        })
        .then(data => data)
        .catch(error => {
            console.error("Erro na requisição:", error);
            throw error;
        });
}

function renderProducts(products) {
    const container = document.querySelector(".product-grid");

    products.forEach(product => {
        const productHtml = `
            <a href="${product.url}" class="product_card">
                <div class="image-container">
                    <img src="/${product.first_image_url}" alt="${product.name}">
                </div
                <div>
                    <h3>${product.name}</h3>
                    <p>R$ ${product.price}</p>
                </div>
            </a>
        `;
        container.insertAdjacentHTML("beforeend", productHtml);
    });
}
