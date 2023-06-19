(function ($) {
    $(document).ready(function(){


// Function to calculate the sum of Quantity * Price and set the value in PriceTotal fields
function calculateTotal() {
  var rows = document.querySelectorAll("tbody tr.has_original"); // Select all rows with class 'has_original'
  var total = 0;

  rows.forEach(function(row) {
    var quantity = parseInt(row.querySelector(".field-Quantity input").value);
    var price = parseFloat(row.querySelector(".field-Price input").value);
    var priceTotalField = row.querySelector(".field-PriceTotal input");
    
    if (!isNaN(quantity) && !isNaN(price)) {
      var priceTotal = quantity * price;
      total += priceTotal;
      priceTotalField.value = priceTotal.toFixed(4);
    }
  });

  // Set the calculated total in the input field
  document.getElementById("id_TotalAmount").value = total.toFixed(4);
}

// Add event listeners to Quantity and Price input fields
var quantityInputs = document.querySelectorAll(".field-Quantity input");
var priceInputs = document.querySelectorAll(".field-Price input");

quantityInputs.forEach(function(input) {
  input.addEventListener("input", function() {
    calculateTotal();
    var row = input.closest("tr");
    var priceTotalField = row.querySelector(".field-PriceTotal input");
    priceTotalField.value = (parseInt(input.value) * parseFloat(row.querySelector(".field-Price input").value)).toFixed(4);
  });
});

priceInputs.forEach(function(input) {
  input.addEventListener("input", function() {
    calculateTotal();
    var row = input.closest("tr");
    var priceTotalField = row.querySelector(".field-PriceTotal input");
    priceTotalField.value = (parseInt(row.querySelector(".field-Quantity input").value) * parseFloat(input.value)).toFixed(4);
  });
});





        $('#id_CustomerName, #id_Address').on('change',function(){
            var initialname = $('#id_CustomerName').val();
            var initialquantity = $('#id_Address').val();
            if (initialname !== '' && initialquantity !== '') {
                $.ajax({
                    type: 'POST',
                    url: '/library/ajax/',
                    data: {
                        'name': initialname,
                        'quantity': initialquantity
                    },
                    dataType: 'json',
                    success: function(response){
                        // updateFormset(response);
                        // $('#id_production_components-0-quantity').val(response.quantity);

                    }
                });
            }

        });



    });
})(jQuery);