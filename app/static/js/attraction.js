// attraction.html 透過 fetch 抓取該 id 對應的 api
// let originURL = window.location.origin;
const currentPath = window.location.pathname;
const name = document.querySelector('.name');
const category = document.querySelector('.category');
const mrt = document.querySelector('.mrt');
const description = document.querySelector('.description');
const address = document.querySelector('.address');
const transport = document.querySelector('.transport');

// const attractionImages = document.getElementById('attraction-images');
const imagesContainer = document.getElementById('images-container');
const arrowLeft = document.getElementById('arrow-left');
const arrowRight = document.getElementById('arrow-right');

let currentImageIndex = 0;
let numImages = 0;
let images = [];
let attractionId;
const dotsContainer = document.getElementById('dots');

// 取得景點
async function getAttractionId(){
    try{
        const response = await fetch(`${originURL}/api${currentPath}`);

        if(!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        let attraction = await response.json();
        attraction = attraction.data[0];

        images = attraction.images;
        numImages = images.length;

        name.textContent = attraction.name;
        category.textContent = attraction.category;
        mrt.textContent = attraction.mrt;
        description.textContent = attraction.description;
        address.textContent = attraction.address;
        transport.textContent = attraction.transport;
        // attractionImages.src = images[currentImageIndex];

        document.title = attraction.name; 
        attractionId = attraction.id;
        // 圖片

        for(let i=0; i<numImages; i++){
            const imageContainer = document.createElement('div');
            imageContainer.classList.add('image-container')

            const attractionImages = document.createElement('img');
            attractionImages.src = images[i];

            imageContainer.appendChild(attractionImages);
            imagesContainer.appendChild(imageContainer);
        }

        generateDots();

    } catch(error){
        console.error('獲取景點數據時出錯：', error);
    }
}

getAttractionId();

// 按照圖片數量產生相同數量的點點
function generateDots(){
    for(let i = 0; i < numImages; i++){
        const dot = document.createElement('img');
        dot.classList.add('dot');
        dot.src = "../img/circle.svg";
        if(i === 0){
            dot.classList.add('check');
            dot.src = "../img/circle-check.svg";
        }
        dotsContainer.appendChild(dot);
    }
}

function updateDots(index){
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, index) =>{
        if(index === currentImageIndex){
            dot.classList.add('check');
            dot.src = "../img/circle-check.svg";
        } else {
            dot.classList.remove('check');
            dot.src = "../img/circle.svg";
        }
    });
}
// 將第一張照片顯示，其他照片隱藏在右邊，當點選右箭頭時跳至下一張，左箭頭跳至前一張
arrowRight.addEventListener('click',() => {
    currentImageIndex = (currentImageIndex + 1) % numImages;
    updateImagesTransform();
    updateDots(currentImageIndex);
});

arrowLeft.addEventListener('click', () => {
    currentImageIndex = (currentImageIndex - 1 + numImages) % numImages;
    updateImagesTransform();
    updateDots(currentImageIndex);
});  

function updateImagesTransform(){
    const translateX = -currentImageIndex * 100;
    imagesContainer.style.transform = `translateX(${translateX}%)`; 
};


// 若選擇時間選下半天，則導覽費用改為2500元
const firstHalfDay = document.getElementById('first-half-day');
const secondHalfDay = document.getElementById('second-half-day');
const guideFee = document.getElementById('guide-fee');
let guideFeeValue = 2000;

function updateGuideFee(){
    if(firstHalfDay.checked){
        guideFeeValue = 2000;
    }else if(secondHalfDay.checked){
        guideFeeValue = 2500;
    }
    guideFee.textContent = `新台幣 ${guideFeeValue} 元`;
}
let inputDate = document.getElementById('date');
// 計算當天
function currentDate(){
    const currentDate = new Date();

    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth()+1).padStart(2,'0');
    const day = String(currentDate.getDate()).padStart(2,'0');

    const formattedDate = `${year}-${month}-${day}`;
    inputDate.min = formattedDate;
    inputDate.value = formattedDate;
}
currentDate()


document.addEventListener('DOMContentLoaded', function(){
    const bookingForm = document.getElementById('booking-form');
    let selectDate;
    
    bookingForm.addEventListener('submit', function(e){
        e.preventDefault();

        selectDate = new Date(inputDate.value);

        if(!validdateDate()){
            return;
        }
        if(!userLoggedIn){
            toggleDisplay(loginBox,'block');
        } else {
            createbooking();
        }
    });
    

    function validdateDate(){
        if(!date){
            alert('請選擇日期。');
            return false
        } 
        return true;
    }

    async function createbooking(){

        try {
            const time = document.querySelector('input[name="time"]:checked').value;
            const formattedDate = selectDate.toISOString().split('T')[0];
    
            const bookingData = {
                attractionId:attractionId,
                date: formattedDate,
                time: time,
                price: guideFeeValue
            };
    
            const response = await fetch(`${originURL}/api/booking`,{
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${localStorage.getItem('Token')}`
                },
                body: JSON.stringify(bookingData)
            });

            if(response.ok){
                window.location.href = '/booking';

                
            } else {
                
                console.error('預定失敗', error);
            }
        } catch(e){
            console.error('預定失敗', e.message);
        }

    }
});

