function getAuthenticationToken() {
    const Http = new XMLHttpRequest();
    const url='/account/get_token';
    Http.open("GET", url);
    Http.send();
    Http.onreadystatechange=(e)=>{
        document.getElementById("token_area").innerText = Http.responseText;
    }
}

document.getElementById("get_token_button").addEventListener("click", getAuthenticationToken);