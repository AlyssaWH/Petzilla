'use strict';

$('.add-pharm').on('submit', evt => {
    evt.preventDefault();
    console.log("do it work?")
  
    const formValues = $(`.add-pharm`).serialize();
   
    const petid = $('#pet_id').val();
    // (${expression}
    $.post(`/pets/${petid}`, formValues, res => {
      alert(res);  
      $('.pharm').html(res);
      // find the div and make it show up on the page itself
    });
  });

 

  $('.add-pet').on('submit', evt => {
    
  
   


  const nameInput = document.querySelector('input[name="pet-name"]');

  if (nameInput.value.length < 1) {
    evt.preventDefault();
    alert('Pet name must be entered');
  }});

