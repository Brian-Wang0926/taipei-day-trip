let originURL = window.location.origin;
// 建立 userloggin
let userLoggedIn = false;

const loginButton = document.querySelector('.nav-login-button')

const closeLoginButton = document.querySelector('.close-login')
const closeSignupButton = document.querySelector('.close-signup')

const loginBox = document.getElementById('login')
const signupBox = document.getElementById('signup')

const toSignup = document.getElementById('to-signup')
const toLogin = document.getElementById('to-login')

function toggleDisplay(element, displayValue){
    element.style.display = displayValue;
}

loginButton.addEventListener('click', () =>{
    if(userLoggedIn){
        logout()
    } else {
        toggleDisplay(loginBox, 'block');
    }
});


closeLoginButton.addEventListener('click', () => toggleDisplay(loginBox,'none'));
closeSignupButton.addEventListener('click', () => toggleDisplay(signupBox,'none'));

toSignup.addEventListener('click', () => {
    toggleDisplay(loginBox,'none');
    toggleDisplay(signupBox, 'block');
});
toLogin.addEventListener('click', () => {
    toggleDisplay(loginBox,'block');
    toggleDisplay(signupBox, 'none');
});

// 註冊會員
// 當 user填寫資料按送出後，會將資料 fetch 至 註冊api
// 後端檢查 email 是否和資料庫重複，若沒有則將資料存入資料庫
const signupForm = document.getElementById('signup-form');
const signupMessage = document.getElementById('signup-message');

signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    signup(name, email, password);
});

async function signup(name, email, password){
    try{
        const response = await fetch(`${originURL}/api/user`, {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({
                name, email, password
            })
        });

        const responseData = await response.json();
        console.log(responseData);

        if(responseData.error){
            signupMessage.style.color = 'red';
        } else {
            signupMessage.style.color = 'green';
        }

        signupMessage.textContent = responseData.message;

    } catch(error){
        console.error('註冊失敗', error)
    }
}

const loginForm = document.getElementById('login-form');
const loginMessage = document.getElementById('login-message');

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    login(email, password);
});

async function login(email, password){
    try{
        const response = await fetch(`${originURL}/api/user/auth`, {
            method: 'PUT',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({
                email, password
            })
        });

        const responseData = await response.json();
        console.log("登入成功： ",responseData);

        if(responseData.error){
            loginMessage.style.color = 'red';
        } else {
            const token = responseData.token;
            localStorage.setItem('Token', token);

            userLoggedIn = true;
            updateLoginButtonText();

            loginButton.addEventListener('click', logout);
            toggleDisplay(loginBox,'none');
        }

        loginMessage.textContent = responseData.message;

    } catch(error){
        console.error('登入失敗', error);
    }
}

function logout(){
    if(userLoggedIn){
        localStorage.removeItem('Token');
        toggleDisplay(loginBox,'none');
        loginButton.removeEventListener('click', logout);
    
        userLoggedIn = false;
        userStatus();
        updateLoginButtonText();
    
        console.log("登出成功");
    }
}

window.addEventListener('load', () => {
    userStatus();
    updateLoginButtonText();
});

// 檢查會員登入狀態流程
async function userStatus(){
    try{
        const token = localStorage.getItem('Token');

        if(token) {
            const response = await fetch (`${originURL}/api/user/auth`, {
                method:'GET',
                headers: {
                    'Authorization': `Bearer ${token}` 
                }
            });
        
                // const responseData = await response.json();
            if (response) {
                console.log("前端：仍在登入中 ");
                // 如果后端返回状态码为 200，表示用户已登录
                userLoggedIn = true;
                updateLoginButtonText();
            } else {
                // 如果状态码不是 200，表示用户未登录
                console.log("前端：未登入 ");
                userLoggedIn = false;
                updateLoginButtonText();
            }
        } else {
            // 如果没有 token，表示用户未登录
            userLoggedIn = false;
            updateLoginButtonText();
        }
    } catch(error) {
        userLoggedIn = false;
        updateLoginButtonText();
        console.error('檢查用戶登入狀態失敗', error);
    }
}

function updateLoginButtonText(){
    if(userLoggedIn){
        loginButton.textContent = '登出系統';
    } else {
        loginButton.textContent = '登入/註冊';
    }
}

