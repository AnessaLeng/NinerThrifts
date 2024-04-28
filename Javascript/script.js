'use strict';

const url = 'https://api.imgbb.com/1/upload';
const API_KEY = 'a6ed1d71a6eea38cf76aec39ba45722f';

const submitBtns = document.querySelectorAll('.api');
submitBtns.addEventListener('click', fetchImg);

async function fetchImg(e){
    const form = document.querySelectorAll('form');
    const formdata = new FormData(form);
    url += `?key=${API_KEY}`;
    try{
        const response = await fetch(url, {
            method: 'POST',
            body: formdata
        });
        if(!response.ok){
            throw Error(`Error: ${response.url} ${response.statusText}`);
        }
        const data = await response.json();
        console.log(data);
    }
    catch(error){
        console.log(error.message);
    }
}