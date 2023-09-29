"use strict"

const originURL = window.location.origin;
// 建立 userloggin
let userLoggedIn = false;

const loginButton = document.querySelector('.nav-login-button')
const loginBox = document.getElementById('login')
const signupBox = document.getElementById('signup')

function toggleDisplay(element, displayValue){
    element.style.display = displayValue;
}

// 關閉 登入/註冊 視窗
 document.body.addEventListener('click',(e) => {
    if(e.target.classList.contains('close-login')){
        toggleDisplay(loginBox,'none');
    } else if (e.target.classList.contains('close-signup')){
        toggleDisplay(signupBox,'none');
    }
 });
//  切換 登入/註冊 視窗
document.body.addEventListener('click', (e) => {
    if(e.target.classList.contains('to-signup')){
        toggleDisplay(loginBox,'none');
        toggleDisplay(signupBox, 'block');
    } else if(e.target.classList.contains('to-login')){
        toggleDisplay(loginBox,'block');
        toggleDisplay(signupBox, 'none');
    }
});
// 若已登入，點擊則登出，否則開啟登入視窗
loginButton.addEventListener('click', () => {
    if(userLoggedIn){
        logout();
    } else {
        toggleDisplay(loginBox, 'block');
    }
});

// 取得會員資料
function getUserInput(selector){
    return document.querySelector(selector).value;
}
// 取得會員註冊資料
async function handleSignup(e){
    e.preventDefault();
    console.log("開始執行")
    const name = getUserInput('#signup-name');
    const email = getUserInput('#signup-email');
    const password = getUserInput('#signup-password');
    console.log("註冊",name, email, password)
    try {
        const responseData = await signup(name, email, password);
        console.log("取得使用者資訊",responseData)
        updateSignupMessage(responseData);
    } catch(error) {
        console.error('註冊失敗', error);
    }
}

// 取得會員登入資料
async function handleLogin(e){
    e.preventDefault();
    const email = getUserInput('#login-email');
    const password = getUserInput('#login-password');

    try {
        const responseData = await login(email, password);

        if(responseData.error){
            console.log("登入失敗",responseData.message);
            updateLoginMessage(responseData);
        } else {
            const token = responseData.token;
            localStorage.setItem('Token', token);
    
            userLoggedIn = true;
            console.log("登入成功", userLoggedIn, token)
            updateLoginButtonText();
            toggleDisplay(loginBox,'none');
        }
    } catch(error) {
        console.error('登入失敗', error);
    }
}

// 整合註冊和登入功能
async function performUserAction(url, method, data){
    try{
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        });
        console.log("performUserAction執行完畢", response)
        return await response.json();
    } catch(error) {
        throw error;
    }
}
async function signup(name, email, password){
    const url = `${originURL}/api/user`;
    const data = { name, email, password };
    return await performUserAction(url, 'POST', data)
}
async function login(email, password){
    console.log("login fetch開始")
    const url = `${originURL}/api/user/auth`;
    const data = { email, password };
    console.log("登入資料",email,password);
    return await performUserAction(url, 'PUT', data)
}

function updateSignupMessage(responseData){
    const messageElement = document.getElementById('signup-message');
    messageElement.style.color = responseData.error ? 'red' : 'green';
    messageElement.textContent = responseData.message;
}

function updateLoginMessage(responseData){
    const messageElement = document.getElementById('login-message');
    messageElement.style.color = responseData.error ? 'red' : 'green';
    messageElement.textContent = responseData.message;
}

const signupForm = document.getElementById('signup-form');
signupForm.addEventListener('submit', handleSignup);

const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', handleLogin);

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
    userLoggedIn = checkUserLoggedin();
    console.log(userLoggedIn);
    userStatus();
    updateLoginButtonText();
});

function checkUserLoggedin(){
    const token = localStorage.getItem('Token');
    return !!token; //回覆 boolean
}

// 檢查會員登入狀態流程
async function userStatus(){
    try{
        const token = localStorage.getItem('Token');
        console.log("目前登入狀態", userLoggedIn);
        if(token) {
            const response = await fetch (`${originURL}/api/user/auth`, {
                method:'GET',
                headers: {
                    'Authorization': `Bearer ${token}` 
                }
            });
        
            if (response) {
                console.log("前端：仍在登入中 ");
                // 如果后端返回状态码为 200，表示用户已登录
                userLoggedIn = true;
            }
        } else {
            // 如果没有 token，表示用户未登录
            userLoggedIn = false;

        }
    } catch(error) {
        userLoggedIn = false;
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

// 點擊預定行程，會跳轉到booking.html
const bookingButton = document.querySelector('.nav-booking-button');

bookingButton.addEventListener('click', () => {
    userStatus();
    if(!userLoggedIn){
        toggleDisplay(loginBox,'block');
    } else {
        window.location.href = '/booking'
    }
});
