document.addEventListener('DOMContentLoaded', function () {
    document.querySelector("#sell_online").addEventListener('click', fsell_online);
})

function fsell_online() {
    
    document.querySelector("#active_listing_div").style.display = 'none';
    document.querySelector("#sell_online_div").style.display = 'block';
}

function index() {
    document.querySelector("#active_listing_div").style.display = 'block';
    document.querySelector("#sell_online_div").style.display = 'none';
}