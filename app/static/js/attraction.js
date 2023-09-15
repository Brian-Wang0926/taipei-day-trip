// attraction.html 透過 fetch 抓取該 id 對應的 api
let originURL = window.location.origin;
const currentPath = window.location.pathname;

const name = document.querySelector('.name');
const category = document.querySelector('.category');
const mrt = document.querySelector('.mrt');
const description = document.querySelector('.description');
const address = document.querySelector('.address');
const transport = document.querySelector('.transport');

const attractionImages = document.getElementById('attraction-images');
const arrowLeft = document.getElementById('arrow-left');
const arrowRight = document.getElementById('arrow-right');

let currentImageIndex = 0;
let numImages = 0;
let images = [];

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
        attractionImages.src = images[currentImageIndex];

        document.title = attraction.name; 
        
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
        console.log(numImages);
    }
}

// 將第一張照片顯示，其他照片隱藏在邊，當點選右箭頭時跳至下一張，左箭頭跳至前一張
arrowRight.addEventListener('click',() => {
    currentImageIndex++;
    if (currentImageIndex < numImages ){
        attractionImages.src = images[currentImageIndex];
        updateDots(currentImageIndex);
    } else {
        currentImageIndex = 0;
        attractionImages.src = images[currentImageIndex];
        updateDots(currentImageIndex);
        // currentImageIndex = numImages - 1;
    }          
});

arrowLeft.addEventListener('click', () => {
    currentImageIndex--;
    if (currentImageIndex >= 0 ){
        attractionImages.src = images[currentImageIndex];
        updateDots(currentImageIndex);
    } else {
        currentImageIndex = numImages - 1;
        attractionImages.src = images[currentImageIndex];
        updateDots(currentImageIndex);
    }     
});  

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

// 若選擇時間選下半天，則導覽費用改為2500元
const firstHalfDay = document.getElementById('first-half-day');
const secondHalfDay = document.getElementById('second-half-day');
const guideFee = document.getElementById('guide-fee');

function updateGuideFee(){
    if(firstHalfDay.checked){
        guideFeeValue = 2000;
    }else if(secondHalfDay.checked){
        guideFeeValue = 2500;
    }
    guideFee.textContent = `新台幣 ${guideFeeValue} 元`;
}

