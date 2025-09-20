function changeCount(id, delta) {
    const input = document.getElementById('count_' + id);
    let value = parseInt(input.value) + delta;
    if (value < 0) value = 0;
    input.value = value;
    updateTotal();
}

function updateTotal() {
    let total = 0;
    const items = document.querySelectorAll('.dish');
    items.forEach(dish => {
        const count = parseInt(dish.querySelector('input[type="number"]').value);
        const price = parseFloat(dish.dataset.price);
        total += count * price;
    });
    document.getElementById('total').innerText = total.toFixed(2);
}