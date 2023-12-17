function updateTotalPrice() {
  const nettoPrisElement = document.getElementById("netto");
  const cartItems = document.querySelectorAll(".cart-item");
  let total = 0;

  let orders = []; // JavaScript array

  // bygger JSON op med alle produkter i kurven
  cartItems.forEach((item) => {
    let order = {}; // opretter et JavaScript objekt for hvert produkt
    const itemPrice = parseFloat(
      item.querySelector(".cart-price").textContent.replace(" kr.", "")
    );

    order.qnty = item.querySelector(".cart-quanity").textContent;
    order.title = item.querySelector(".cart-title").textContent;

    total += itemPrice;
    order.price = itemPrice;
    orders.push(order);
  });
  //orders er nu et array af JavaScript objekter
  let orderJSON = JSON.stringify(orders); // Vi laver nu JavaScript arrayet objekterne om til JSON streng
  // Vi gemmer JSON i session storage til senere brug i checkout skjult input felt
  sessionStorage.setItem("orderJSON", orderJSON);

  nettoPrisElement.textContent = total.toFixed(2) + " kr.";

  // Store the total value in localStorage
  sessionStorage.setItem("nettoAmount", total.toFixed(2) + " kr.");

  // Update the total in parentheses
  updateTotalInParentheses();
}
