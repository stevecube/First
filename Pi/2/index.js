let check = document.getElementById('check');
let output = document.getElementById('p');

check.addEventListener('click', function(){
    a = 3.14;
    let input = document.getElementById('input').value;
    if(input == a){
        output.innerHTML = 'You are correct';
    }else{
        output.innerHTML = 'You are incorrect, please try again';
    }
});