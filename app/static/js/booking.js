// fetch 抓取得預定景點 api
// (token取得)將姓名、信箱
// 到資料庫抓 景點第一張照片、景點名稱、日期、時間、費用、地點 並轉進 booking
const nameElement = document.getElementById('name');
const pic = document.querySelector('#pic');
const date = document.getElementById('date');
const time = document.getElementById('time');
const fee = document.getElementById('guide-fee');
const address = document.getElementById('address');
const attractionName = document.getElementById('attraction-name');
const token = localStorage.getItem('Token');
const nameInput = document.getElementById('name_input');
const emailInput = document.getElementById('email');
const totalPriceElement = document.getElementById('total-price');

window.addEventListener('load', async () => {
    userLoggedIn = await checkUserLoggedin();

    if (!userLoggedIn) {
        window.location.href = '/';
    } else {
        getBookingData();
    }
});

async function getBookingData(){
    try {
        let response = await fetch(`${originURL}/api/booking`,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${localStorage.getItem('Token')}`
            },
        });

        let data = await response.json();
        let bookingData = data.data;
        const noBookingMessage = document.getElementById('no-booking-message');
        const separateLineElements = document.querySelectorAll('.separate-line');
        const bookingContactElement = document.querySelector('.booking-contact');
        const bookingPaymentElement = document.querySelector('.booking-payment');
        const confirmElement = document.querySelector('.confirm');

        nameElement.textContent = data.user_name;
        nameInput.value = data.user_name;
        emailInput.value = data.user_email;

        if(bookingData == null){
            noBookingMessage.textContent = '目前沒有任何行程';
            separateLineElements.forEach(element => {
                element.style.display = 'none'; 
            });
            bookingContactElement.style.display = 'none'; // 隱藏聯絡資訊
            bookingPaymentElement.style.display = 'none'; // 隱藏付款資訊
            confirmElement.style.display = 'none'; // 隱藏確認訂購區域
        } else {

            let totalPrice = 0;

            // 建立預定景點
            const bookingContainer = document.getElementById('booking-container');
            bookingContainer.innerHTML = '';

            bookingData.forEach(booking => {
                const bookingAttraction = document.createElement('div');
                bookingAttraction.classList.add('booking-attraction');

                // 刪除預定景點
                const deleteIcon = document.createElement('img');
                deleteIcon.classList.add('icon-delete');
                deleteIcon.src = "../img/icon-delete.svg";
                deleteIcon.alt = "刪除景點";

                // 點擊按鈕後，取得 bookingID，並透過 bookingID到資料庫刪除預定景點
                deleteIcon.dataset.bookingId = booking.booking_id;

                const bookingId = deleteIcon.dataset.bookingId;
                deleteIcon.addEventListener('click',() => deleteBooking(bookingId));

                // 照片
                const picElement = document.createElement('div');
                picElement.classList.add('pic');
                const imgElement = document.createElement('img');
                imgElement.id = 'pic';
                imgElement.src = booking.attraction.pic;
                imgElement.alt = '景點照片';
                picElement.appendChild(imgElement);

                // 預定景點資訊
                const inforElement = document.createElement('div');
                inforElement.classList.add('infor');

                const attractionNameElement =  document.createElement('h4');
                attractionNameElement.id = 'attraction-name';
                attractionNameElement.textContent = `台北一日遊：${booking.attraction.attraction_name} `;

                const dateElement = document.createElement('span');
                dateElement.id = 'date';
                dateElement.textContent = `日期：${booking.date}`;

                const timeElement = document.createElement('span');
                timeElement.id = 'time';
                const timeText = booking.time === 'morning' ? '早上 9 點到中午 12 點' : "下午 1 點到下午 5 點";
                timeElement.textContent = `時間：${timeText}`;

                const feeElement = document.createElement('span');
                feeElement.id = 'guide-fee';
                feeElement.textContent = `費用：新台幣 ${booking.price} 元`;
                totalPrice += booking.price;

                const addressElement = document.createElement('span');
                addressElement.id = 'address';
                addressElement.textContent = `地址：${booking.attraction.attraction_address} `;

                inforElement.appendChild(attractionNameElement);
                inforElement.appendChild(dateElement);
                inforElement.appendChild(timeElement);
                inforElement.appendChild(feeElement);
                inforElement.appendChild(addressElement);

                bookingAttraction.appendChild(deleteIcon);
                bookingAttraction.appendChild(picElement);
                bookingAttraction.appendChild(inforElement);

                bookingContainer.appendChild(bookingAttraction);
            });
            
            totalPriceElement.textContent = `總價：新台幣 ${totalPrice} 元`;
        }
    } catch(e) {
        console.error('預定失敗', e.message);
    }
}

loginButton.addEventListener('click', () => {
    if(userLoggedIn == false){
        window.location.href = '/';
    };
});

async function deleteBooking(bookingId){
    console.log("刪除預定景點", bookingId);

    await fetch(`${originURL}/api/booking/${bookingId}`,{
        method:'DELETE',
        headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${localStorage.getItem('Token')}`
        }
    })
    .then(response => {
        if(response.ok){
            console.log("刪除成功");
            window.location.href = '/booking';
        } else {
            console.error("刪除失敗");
        }
    })
    .catch(error => {
        console.error("刪除失敗");
    });
};

