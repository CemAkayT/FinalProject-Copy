// definerer en funktion
function updateTotalPrice() {
  // Henter reference til HTML-elementet med id 'netto' fra home.html og gemmer den i variablen 'nettoPrisElement'
  const nettoPrisElement = document.getElementById("netto");

  // Henter alle HTML-elementer med klassen 'cart-item' (dette er kurvvarerne)
  // 'querySelectorAll' finder alle med samme klasse
  const cartItems = document.querySelectorAll(".cart-item");

  // Initialiserer variabelen 'total' til 0 for at beregne den samlede pris
  // Denne variabel vil blive brugt til at beregne den samlede pris for alle varerne i kurven.
  let total = 0;

  // Opret et tomt Javascript array 'orders' til at gemme oplysninger om produkterne i kurven
  let orders = [];

  // bygger JSON op med alle produkter i kurven
  // Itererer over hvert 'cart-item' element i kurven
  cartItems.forEach((item) => {

    // inde i løkken oprettes et tomt JavaScript objekt for hvert produkt
    let order = {};

    // Finder prisen for hvert produkt og fjerner teksten ' kr.'
    const itemPrice = parseFloat(
      item.querySelector(".cart-price").textContent.replace(" kr.", "")
    );

    // Gemmer kvantitet og titel for produktet i 'order' objektet
    order.qnty = item.querySelector(".cart-quanity").textContent;
    order.title = item.querySelector(".cart-title").textContent;

    // Beregner den samlede pris ved at tilføje den enkelte vares pris til 'total
    total += itemPrice;

    // Gem produktinformationen i 'orders' arrayet
    order.price = itemPrice;
    orders.push(order);
  });

  //orders er nu et array af JavaScript objekter med produktinformation
  // Konverterer 'orders' til en JSON-streng
  let orderJSON = JSON.stringify(orders);

  // Gemmer JSON-strengen i session storage  med nøglen 'orderJSON' til senere brug i checkout (skjult inputfelt)
  sessionStorage.setItem("orderJSON", orderJSON);

  // Opdater HTML-elementet med id 'netto' med den samlede pris i formatet 'x.xx kr.'
  nettoPrisElement.textContent = total.toFixed(2).replace(".", ",") + " kr.";

  // Gemmer den samlede pris i localStorage (sessionStorage bruges her)
  // sessionStorage.setItem("nettoAmount", total.toFixed(2) + " kr.");
  sessionStorage.setItem("nettoAmount", total.toFixed(2).replace(".", ",") + " kr.");

  // Opdaterer den samlede pris i parenteser (kalder en anden funktion)
  updateTotalInParentheses();
}
