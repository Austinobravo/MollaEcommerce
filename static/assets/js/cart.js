var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId= this.dataset.product
        var action= this.dataset.action
        console.log('productId:', productId, 'action:', action)
        
        console.log('USER:', user)
        if( user === "AnonymousUser"){
            addCookieItem(productId, action)

        }else{
            UpdateUserOrder(productId,action)
        }
    })
}
function addCookieItem(productId, action){
    console.log('Anonymous User, Please Register');

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
    }
     if(action == 'delete'){
         delete cart[productId]

     }
    console.log('cart:', cart);
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
    //document.getElementById('total-items').innerText = data['cartTotal']

}

function UpdateUserOrder(productId, action){
    console.log('Logged in');

    var url = '/update_item/'

    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
        //document.getElementById('total-items').innerText = data['cartTotal']

    })
}

