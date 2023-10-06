document.addEventListener("DOMContentLoaded", async () => {
  const orderNumberElement = document.getElementById("order-number");
  const token = localStorage.getItem("Token");
  const currentURL = window.location.href;
  const url = new URL(currentURL);
  const orderNumber = url.searchParams.get("number");

  orderNumberElement.textContent = `訂單編號：${orderNumber}`;

  userLoggedIn = await checkUserLoggedin();
  if (!userLoggedIn) {
    window.location.href = "/";
  } else {
    console.log("前端取得資料");
    getOrderData();
  }

  async function getOrderData() {
    try {
      console.log("開始fetch");
      let response = await fetch(`${originURL}/api/order/${orderNumber}`);
      console.log("fetch回傳", response);
    
      let order = await response.json();
    } catch (e) {
      console.log(e);
    }
  }
});
