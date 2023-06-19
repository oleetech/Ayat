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
        });
      }
  
      // Call the function to handle field changes
      handleFieldChanges();
    });
  })(jQuery);
  