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


