(function(){
    window.toggleModal = function (type) {
        let miniQrcode = document.getElementById('mini-qrcode')
        if (type == 1 ) {
            miniQrcode.style.display = 'block'
        } else {
            miniQrcode.style.display = 'none'
        }
    }
})();