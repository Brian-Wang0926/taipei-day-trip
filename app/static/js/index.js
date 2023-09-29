// "use strict"

// list-bar
async function getMrtList() {
    try {
        const response = await fetch(`${originURL}/api/mrts`);
        if(!response.ok){
            throw new Error('HTTP error ' + response.status);
        }
    
        const mrt = await response.json();
        const mrtList = document.getElementById('mrt-list');

        mrt.data.forEach(mrt => {

            const mrtDiv = document.createElement('div');
            mrtDiv.className = 'mrt-div';
            mrtDiv.textContent = mrt;

            mrtList.appendChild(mrtDiv)

        });
    }catch (error) {
        console.error('發生錯誤：', error);
    }
}
getMrtList()


// arrow
const arrowLeft = document.getElementById('arrow-left');
const arrowRight = document.getElementById('arrow-right');
const mrtList = document.getElementById('mrt-list');
let scrollAmount = calculateScrollAmount();

function calculateScrollAmount(){
    let mrtListWidth = mrtList.scrollWidth;
    return mrtListWidth * 2/3;
}

window.addEventListener('resize', () => {
    scrollAmount = calculateScrollAmount();
});

function ArrowClick(direction){
    const currentScroll = mrtList.scrollLeft;
    console.log("目前滾輪位置：", currentScroll);
    const step = scrollAmount;

    if(direction === 'left'){
        const targetScroll = currentScroll - step;
        mrtList.scrollTo({
            left: targetScroll,
            behavior: "smooth",
        });
    
    }else{
        const targetScroll = currentScroll + step;
        mrtList.scrollTo({
            left: targetScroll,
            behavior: "smooth",
        });
    }
}
arrowLeft.addEventListener('click', () => ArrowClick('left'));
arrowRight.addEventListener('click', () => ArrowClick('right'));


// attractions
let keyword = '';
let nextPage = 0;
let isLoading = false; //判斷是否正在載入

// 關鍵字查詢
const keywordInput = document.getElementById('keyword-input');
const searchBar = document.getElementById('search-bar');
const attractionsGroup = document.getElementById('attractions-group');

searchBar.addEventListener('submit', (e) => {
    e.preventDefault();
    keyword = keywordInput.value;
    nextPage = 0;  // 重置頁面

    attractionsGroup.innerHTML = '';
    
    getAttractions();
});

// 取得景點
async function getAttractions() {
    try {
        const response = await fetch(`${originURL}/api/attractions?page=${nextPage}&keyword=${keyword}`);
        if(!response.ok){
            throw new Error('HTTP error ' + response.status);
        }
    
        const attractions = await response.json();
        const attractionsGroup = document.getElementById('attractions-group');
        
        nextPage = attractions.nextPage;
        if(attractions.data.length === 0){
            attractionsGroup.innerHTML = '<p>查無資料</p>';
        }else{
            attractions.data.forEach(attraction => {
            // // 創建 id 以供點擊後跳轉
            const id = attraction.id;

            // 創建 main-div
            const mainDiv = document.createElement('div');
            mainDiv.className = 'main-div';
            mainDiv.setAttribute('id', id);

            mainDiv.addEventListener('click', mainDivClick);
            
            // 創建 first-div
            const firstDiv = document.createElement('div');
            firstDiv.className = 'first-div';

            // 創建圖片元素
            const img = document.createElement('img');
            img.className = 'img';
            img.src = attraction.images[0];
            firstDiv.appendChild(img);

            // 創建名稱元素
            const name = document.createElement('div');
            name.className = 'name';
            name.textContent = attraction.name;
            firstDiv.appendChild(name);

            // 創建 second-div
            const secondDiv = document.createElement('div');
            secondDiv.className = 'second-div';

            // 創建 mrt 元素
            const mrt = document.createElement('div');
            mrt.className = 'mrt';
            mrt.textContent = attraction.mrt;
            secondDiv.appendChild(mrt);

            // 創建 category 元素
            const category = document.createElement('div');
            category.className = 'category';
            category.textContent = attraction.category;
            secondDiv.appendChild(category);

            mainDiv.appendChild(firstDiv);
            mainDiv.appendChild(secondDiv);

            attractionsGroup.append(mainDiv)
            
            isLoading = false;

            setTimeout(() => {
                observeBotton();
            }, 300);
        });
    }

    }catch(error){
        console.error('獲取景點數據時出錯：', error);
        isLoading = false;
    }
}    

// 透過 IntersectionObserver 偵測若頁面捲動到最下方，自動載入第二頁，並接續顯示
function isAtBottom(entries, observer) {
    if(entries[0].isIntersecting && !isLoading && nextPage !== null){
        isLoading = true;
        getAttractions();
    }
}
function observeBotton(){
    const lastMainDiv = document.querySelector('.main-div:last-child');
    if(lastMainDiv){
        const observer = new IntersectionObserver(isAtBottom);
        observer.observe(lastMainDiv);
    }

}

getAttractions();

// 點擊 mrt 會傳送至 keyword 並跳出查詢結果
mrtList.addEventListener('click', (e) => {
    if(e.target.className === 'mrt-div'){
        keywordInput.value = e.target.textContent;
        searchBar.dispatchEvent(new Event('submit'));
    }
});

// 偵測到點擊圖片後，跳轉到 attraction.html ,並夾帶 id

function mainDivClick(e){
    const id = e.target.closest('.main-div').getAttribute('id');
    window.location.href = `${originURL}/attraction/${id}`;
}
