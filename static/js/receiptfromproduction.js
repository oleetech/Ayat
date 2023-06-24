(function($) {
    $(document).ready(function() {
      // Example: Changing IDs with prefix
      var prefix = '#id_productionreceiptitem_set-';
      var quantityPrefix = '#id_productionreceiptitem_set-{0}-Quantity';
      var pricePrefix = '#id_productionreceiptitem_set-{0}-Price';
      var priceTotalPrefix = '#id_productionreceiptitem_set-{0}-PriceTotal';
  
      // Example: Calculate PriceTotal
      function calculatePriceTotal(index) {
        var quantity = parseFloat($(quantityPrefix.replace('{0}', index)).val());
        var price = parseFloat($(pricePrefix.replace('{0}', index)).val());
        var priceTotal = quantity * price;
        $(priceTotalPrefix.replace('{0}', index)).val(priceTotal.toFixed(4));
      }
  
      // Example: Calculate the sum of all PriceTotal values
      function calculateTotalAmount() {
        var total = 0;
        $('input[name^="productionreceiptitem_set-"][name$="-PriceTotal"]').each(function() {
          var priceTotal = parseFloat($(this).val());
          if (!isNaN(priceTotal)) {
            total += priceTotal;
          }
        });
        return total.toFixed(4);
      }
  
      // Example: Set the TotalAmount value
      function setTotalAmount() {
        var totalAmount = calculateTotalAmount();
        $('#id_TotalAmount').val(totalAmount);
      }
  
      // Example: Handle changes in Quantity and Price fields
      function handleFieldChanges() {
        $('input[name^="productionreceiptitem_set-"][name$="-Quantity"], input[name^="productionreceiptitem_set-"][name$="-Price"]').on('change', function() {
          var index = $(this).attr('name').split('-')[1];
          calculatePriceTotal(index);
          setTotalAmount();
          setTotalQty();
        });
      }
  
       // Example: Set the TotalQty value
function setTotalQty() {
  var totalQty = calculateTotalQty();
  $('#id_TotalQty').val(totalQty);
}

function calculateTotalQty() {
  var total = 0;
  $('input[name^="productionreceiptitem_set-"][name$="-Quantity"]').each(function() {
    var quantity = parseFloat($(this).val());
    if (!isNaN(quantity)) {
      total += quantity;
    }
  });
  return total.toFixed(4);
} 


      // Call the function to handle field changes
      handleFieldChanges();
    });
  })(jQuery);
  


  (function($) {
    $(document).ready(function() {
  
      // Function to handle the change event
      function handleProductionNoChange(rowId) {
        var productionNo = $('#id_productionreceiptitem_set-' + rowId + '-ProductionNo').val();
  
        // Send AJAX request to the server
        $.ajax({
          url: '/production/receipt_production_productionno/productionno/',
          type: 'POST',
          data: {
            'ProductionNo': productionNo
          },
          dataType: 'json',
          success: function(response) {
            $("#id_productionreceiptitem_set-" + rowId + "-ItemCode").val(response.code);
            $("#id_productionreceiptitem_set-" + rowId + "-ItemName").val(response.name);
            $("#id_productionreceiptitem_set-" + rowId + "-Quantity").val(response.quantity);


          },
          error: function(xhr, textStatus, errorThrown) {
            console.log('Error:', errorThrown);
          }
        });
      }    
  
      // Event handler for ProductionNo change events
      $(document).on('change', '.dynamic-productionreceiptitem_set select[id^="id_productionreceiptitem_set-"][id$="-ProductionNo"]', function() {
        // Get the row ID from the select element's ID
        var selectId = $(this).attr('id');
        var rowId = selectId.match(/\d+/)[0];
  
        // Call the handleProductionNoChange function
        handleProductionNoChange(rowId);
        
      });
  
    });
  })(jQuery);
  
  