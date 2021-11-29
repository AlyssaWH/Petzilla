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

  
  
   

    $('.update-medicine').on('submit', evt => {

    const medUpdate = document.querySelector('input[name="update"]');
  
    if (medUpdate.value.length < 1) {
      evt.preventDefault();
      alert('Updated medicine amount required');
    }})

    $('.add-med').on('submit', evt => {

      const dailyDose = document.querySelector('input[name="doses-per-day"]');
      const monthlyDose = document.querySelector('input[name="doses-per-month"]');

      if ((dailyDose.value.length > 0) && (monthlyDose.value.length > 0)) {
        evt.preventDefault();
        alert('Daily OR monthly dose amount only');
      }else{
        if ((dailyDose.value.length ===0) && (monthlyDose.value.length ===0)) {

          evt.preventDefault();
          alert('Must enter a daily or monthly dose');

      }}})

