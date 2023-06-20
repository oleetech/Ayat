(function($) {
    $(document).ready(function() {
      // Your code here
  
      // Example: Changing IDs with prefix
      var prefix = '#id_deliveryitem_set-';
      var pricePrefix = '#id_deliveryitem_set-{0}-Price';
      var quantityPrefix = '#id_deliveryitem_set-{0}-Quantity';
      var priceTotalPrefix = '#id_deliveryitem_set-{0}-PriceTotal';
  
      // Example: Calculate PriceTotal
      function calculatePriceTotal(index) {
        var price = parseFloat($(pricePrefix.replace('{0}', index)).val());
        var quantity = parseFloat($(quantityPrefix.replace('{0}', index)).val());
        var priceTotal = price * quantity;
        $(priceTotalPrefix.replace('{0}', index)).val(priceTotal.toFixed(4));
      }
  
      // Example: Calculate the sum of all calculatePriceTotal values
      function calculateTotalAmount() {
        var total = 0;
        $('input[name^="deliveryitem_set-"][name$="-PriceTotal"]').each(function() {
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
  
      // Example: Handle changes in Price and Quantity fields
      function handleFieldChanges() {
        $('input[name^="deliveryitem_set-"][name$="-Price"], input[name^="deliveryitem_set-"][name$="-Quantity"]').on('change', function() {
          var index = $(this).attr('name').split('-')[1];
          calculatePriceTotal(index);
          setTotalAmount();
        });
      }
  
      // Call the function to handle field changes
      handleFieldChanges();
  
    });
  })(jQuery);
  