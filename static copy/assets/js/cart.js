var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId= this.dataset.product
        var action= this.dataset.action
        console.log('productId:', productId, 'action:', action)
        
        console.log('USER:', user)
        if( user === "AnonymousUser"){
            console.log('No Credentials');

        }else{
            console.log('Logged in');
        }
    })
}