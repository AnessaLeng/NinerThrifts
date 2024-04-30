// 'use strict';

// const url = 'https://api.imgbb.com/1/upload';
// const API_KEY = '74dbf4c5d1d64501792892c0157a27f4';

// const submitBtns = document.querySelectorAll('.api');
// submitBtns.addEventListener('click', fetchImg);

// async function fetchImg(e){
//     const formdata = new FormData(form);
//     url += `&key=${API_KEY}`;

//     try{
//         const response = await fetch(url, {
//             method: 'POST',
//             body: formdata
//         });
//         if(!response.ok){
//             throw Error(`Error: ${response.url} ${response.statusText}`);
//         }
//         const responseData = await response.json();
//         console.log(responseData.data.url);
//     }
//     catch(error){
//         console.log(error.message);
//     }
// }