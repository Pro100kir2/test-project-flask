document.addEventListener("DOMContentLoaded", () => {
    fetch("coupons.json")
        .then(response => response.json())
        .then(data => {
            renderCoupons(data);
        });

    document.getElementById("price-sort").addEventListener("change", function () {
        fetch("coupons.json")
            .then(response => response.json())
            .then(data => {
                let sortedCoupons = [...data];

                if (this.value === "popularity") {
                    sortedCoupons.sort((a, b) => b.bought_count - a.bought_count);
                } else if (this.value === "price-asc") {
                    sortedCoupons.sort((a, b) => (a.price_from || 0) - (b.price_from || 0));
                } else if (this.value === "price-desc") {
                    sortedCoupons.sort((a, b) => (b.price_from || 0) - (a.price_from || 0));
                }

                renderCoupons(sortedCoupons);
            });
    });
});

function renderCoupons(coupons) {
    const container = document.getElementById("coupons-container");
    container.innerHTML = "";

    coupons.forEach(coupon => {
        const couponElement = document.createElement("div");
        couponElement.classList.add("coupon-card");

        couponElement.innerHTML = `
            <img src="${coupon.image_url}" alt="Купон">
            <h3>${coupon.description}</h3>
            <p class="price">${coupon.price_from ? `Цена: ${coupon.price_from} руб.` : "Цена не указана"}</p>
            <p class="discount">${coupon.discount ? `Скидка: ${coupon.discount}%` : ""}</p>
            <p class="bought">Купили: ${coupon.bought_count}</p>
            <p class="time-left">Осталось: ${coupon.time_left}</p>
            <a href="${coupon.url}" target="_blank">Подробнее</a>
        `;

        container.appendChild(couponElement);
    });
}
